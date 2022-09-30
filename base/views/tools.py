import os
import re

from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, HttpResponse
from django.utils.translation import gettext as _
from django.conf import settings
from center.models import Center
from ..forms import CenterForm
from base.sanitize_to_import import SanitizeCsv

from scripts.import_people import run as _import_people


IMPORT_PATH = f"{os.path.dirname(settings.BASE_DIR)}/imports"


@user_passes_test(lambda u: u.is_superuser)
def import_people(request):
    # geting imported files
    txt_files = get_txt_files(f"{IMPORT_PATH}/reports")
    context = {
        "title": _("import people"),
        "entries": get_entries(IMPORT_PATH, txt_files) if txt_files else [],
        "form": CenterForm(),
        "search": "base/searchs/modal_import_people.html",
        "import_path": IMPORT_PATH,
    }

    if request.GET.get("report"):
        _report = request.GET["report"]
        with open(f"{IMPORT_PATH}/reports/{_report}", "r") as _file:
            report_data = _file.readlines()
        context["report_data"] = report_data
        context["show_report"] = "show"

    if request.method == "POST" and request.FILES["import_file"]:
        # get file from request.FILES
        file = request.FILES["import_file"]

        # checking if the file has already been imported
        if file.name in get_all_files(IMPORT_PATH):
            context["error"] = (
                "The '%s' file has already been imported!" % file.name
            )
            return render(request, "base/import_people.html", context)

        # checking if the file is of type .csv
        _file = file.name.split(".")
        if _file[-1] != "csv":
            context["error"] = "The '%s' file is not a .CSV file." % file.name
            return render(request, "base/import_people.html", context)

        # sanitize the file if it is a consistent file
        sf = SanitizeCsv(
            file=file,
            path=f"{os.path.dirname(settings.BASE_DIR)}/imports",
        )

        # checking if the dataframe is ok
        if sf.df is False:
            context["error"] = "The '%s' file is inconsistent!" % file.name
            return render(request, "base/import_people.html", context)

        # if dataframe is ok, adjust data and generate .csv files
        sf.adjust_data()
        sf.generate_files()

        # call script import_people
        center = Center.objects.get(id=request.POST.get("conf_center"))
        _import_people(center.name, file.name.split(".")[0])

        # read report file
        file_name = ".".join(_file[:-1])
        with open(
            f"{IMPORT_PATH}/reports/{file_name}__report.txt", "r"
        ) as _file:
            report_data = _file.readlines()

        context["entries"] = get_entries(
            IMPORT_PATH, get_txt_files(IMPORT_PATH)
        )
        context["report_data"] = report_data
        context["show_report"] = "show"

        return render(request, "base/import_people.html", context)

    return render(request, "base/import_people.html", context)


# handlers
def get_all_files(path):
    return [file for file in os.listdir(path)]


def get_txt_files(path):
    return [file for file in os.listdir(path) if ".txt" in file]


def get_entries(path, files, fields=False):
    """
    fields -> to import only an specific field
    """
    # header of each data imported
    data = ("center", "file", "imported_", "time", "- ")

    entries = []
    for file in files:
        _path = (
            f"{path}/reports/fields/{file}"
            if fields
            else f"{path}/reports/{file}"
        )
        with open(_path, "r") as _file:
            report_data = _file.readlines()
            entry = {"report": file}
            for line in report_data:
                # se a linha começar com algum dos cabeçalhos: tratamento
                if line.startswith(data):
                    _line = line.split(": ")
                    _key = re.findall(r"\w+", _line[0].lower())[0]
                    if _line[0].startswith("imported_on"):
                        _value = datetime.strptime(
                            _line[1].strip(), "%Y-%m-%d %H:%M:%S.%f"
                        )
                    elif _line[1].strip().isdigit():
                        _value = int(_line[1].strip())
                    else:
                        _value = _line[1].strip()
                    entry[_key] = _value
            entries.append(entry)
    return entries


# generate file to download
def download_csv(request, file):
    if request.GET.get("type") == "ue":
        _file = f"used_email__{file}"
        _path = f"{IMPORT_PATH}/used_email/{_file}"
    elif request.GET.get("type") == "we":
        _file = f"without_email__{file}"
        _path = f"{IMPORT_PATH}/without_email/{_file}"
    elif request.GET.get("type") == "de":
        _file = f"duplicate_email__{file}"
        _path = f"{IMPORT_PATH}/duplicate_email/{_file}"
    elif request.GET.get("type") == "se":
        _file = f"to_send_email__{file}"
        _path = f"{IMPORT_PATH}/to_send_email/{_file}"
    response = HttpResponse(open(_path, "rb").read())
    response["Content-Type"] = "text/plain"
    response["Content-Disposition"] = f"attachment; filename={_file}"
    return response
