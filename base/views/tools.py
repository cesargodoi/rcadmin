import os
import re

from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, HttpResponse
from django.utils.translation import gettext as _
from django.conf import settings
from center.models import Center
from ..forms import CenterForm
from rcadmin.common import SanitizeCsv

from scripts.import_persons import run as _import_persons
from scripts.import_fields_to_persons import run as _import_fields_to_persons


IMPORT_PATH = f"{os.path.dirname(settings.BASE_DIR)}/imports"


@user_passes_test(lambda u: u.is_superuser)
def import_persons(request):
    # geting imported files
    txt_files = get_txt_files(f"{IMPORT_PATH}/reports")
    context = {
        "title": _("import persons"),
        "entries": get_entries(IMPORT_PATH, txt_files) if txt_files else [],
        "form": CenterForm(),
        "search": "base/searchs/modal_import_persons.html",
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
            return render(request, "base/import_persons.html", context)

        # checking if the file is of type .csv
        _file = file.name.split(".")
        if _file[-1] != "csv":
            context["error"] = "The '%s' file is not a .csv file." % file.name
            return render(request, "base/import_persons.html", context)

        # sanitize the file if it is a consistent file
        sf = SanitizeCsv(
            file=file,
            path=f"{os.path.dirname(settings.BASE_DIR)}/imports",
        )

        if sf.df is False:
            context["error"] = "The '%s' file is inconsistent!" % file.name
            return render(request, "base/import_persons.html", context)

        sf.adjust_data()
        sf.generate_files()

        # call script import_persons
        center = Center.objects.get(id=request.POST.get("conf_center"))
        _import_persons(center.name, file.name)

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

        return render(request, "base/import_persons.html", context)

    return render(request, "base/import_persons.html", context)


@user_passes_test(lambda u: u.is_superuser)
def import_fields_to_persons(request):
    # geting imported files
    txt_files = get_txt_files(f"{IMPORT_PATH}/reports/fields")
    context = {
        "title": _("import fields to persons"),
        "entries": get_entries(IMPORT_PATH, txt_files, fields=True)
        if txt_files
        else [],
        "form": CenterForm(),
        "search": "base/searchs/modal_import_fields_to_persons.html",
        "import_path": IMPORT_PATH,
    }

    if request.GET.get("report"):
        _report = request.GET["report"]
        with open(f"{IMPORT_PATH}/reports/fields/{_report}", "r") as _file:
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
            return render(
                request, "base/import_fields_to_persons.html", context
            )

        # checking if the file is of type .csv
        _file = file.name.split(".")
        if _file[-1] != "csv":
            context["error"] = "The '%s' file is not a .csv file." % file.name
            return render(
                request, "base/import_fields_to_persons.html", context
            )

        # get fields
        COLUMNS = ["name"]
        COLUMNS += (
            request.POST["columns"].replace(" ", "").split(",")
            if "," in request.POST.get("columns")
            else [request.POST["columns"].replace(" ", "")]
        )

        DATES = (
            request.POST["dates"].replace(" ", "").split(",")
            if "," in request.POST.get("dates")
            else [request.POST["dates"].replace(" ", "") or ""]
        )

        # sanitize the file if it is a consistent file
        sf = SanitizeCsv(
            file=file,
            path=f"{os.path.dirname(settings.BASE_DIR)}/imports",
            columns=COLUMNS,
            dates=DATES,
            fields=True,
        )

        if sf.df is False:
            context["error"] = "The '%s' file is inconsistent!" % file.name
            return render(request, "base/import_persons.html", context)

        sf.adjust_data()
        sf.generate_files()
        # print(sf.df)

        # call script import_persons
        center = Center.objects.get(id=request.POST.get("conf_center"))
        _import_fields_to_persons(center.name, file.name)

        # read report file
        file_name = ".".join(_file[:-1])
        with open(
            f"{IMPORT_PATH}/reports/fields/{file_name}__report.txt", "r"
        ) as _file:
            report_data = _file.readlines()

        context["entries"] = get_entries(
            IMPORT_PATH, get_txt_files(IMPORT_PATH), fields=True
        )
        context["report_data"] = report_data
        context["show_report"] = "show"

        return render(request, "base/import_fields_to_persons.html", context)

    return render(request, "base/import_fields_to_persons.html", context)


# handlers
def get_all_files(path):
    return [file for file in os.listdir(path)]


def get_txt_files(path):
    return [file for file in os.listdir(path) if ".txt" in file]


def get_entries(path, files, fields=False):
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
    print(entries)
    return entries


# generate file to download
def download_csv(request, file):
    if request.GET.get("type") == "ue":
        _file = f"ue__{file}"
        _path = f"{IMPORT_PATH}/used_email/{_file}"
    elif request.GET.get("type") == "we":
        _file = f"we__{file}"
        _path = f"{IMPORT_PATH}/without_email/{_file}"
    response = HttpResponse(open(_path, "rb").read())
    response["Content-Type"] = "text/plain"
    response["Content-Disposition"] = f"attachment; filename={_file}"
    return response
