import os
import re

from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from center.models import Center
from ..forms import CenterForm

from scripts.import_persons import run as _import_persons


@user_passes_test(lambda u: u.is_superuser)
def import_persons(request):
    # geting imported files
    import_path = f"{os.path.dirname(settings.BASE_DIR)}/imports"
    txt_files = get_txt_files(import_path)
    context = {
        "title": _("import persons"),
        "entries": get_entries(import_path, txt_files) if txt_files else [],
        "form": CenterForm(),
        "search": "base/searchs/modal_import_persons.html",
    }

    if request.GET.get("report"):
        _report = request.GET["report"]
        with open(f"{import_path}/{_report}", "r") as _file:
            report_data = _file.readlines()
        context["report_data"] = report_data
        context["show_report"] = "show"

    if request.method == "POST" and request.FILES["import_file"]:
        # get file from request.FILES
        file = request.FILES["import_file"]

        # checking if the file has already been imported
        if file.name in get_all_files(import_path):
            context["error"] = (
                "The '%s' file has already been imported!" % file.name
            )
            return render(request, "base/import_persons.html", context)

        # checking if the file is of type .csv
        _file = file.name.split(".")
        if _file[-1] != "csv":
            context["error"] = "The '%s' file is not a .csv file." % file.name
            return render(request, "base/import_persons.html", context)

        # import file
        fs = FileSystemStorage(location=import_path)
        fs.save(file.name, file)

        # call script import_persons
        center = Center.objects.get(id=request.POST.get("conf_center"))
        _import_persons(center.name, file.name)

        # read report file
        file_name = ".".join(_file[:-1])
        with open(f"{import_path}/{file_name}__report.txt", "r") as _file:
            report_data = _file.readlines()

        context["entries"] = get_entries(
            import_path, get_txt_files(import_path)
        )
        context["report_data"] = report_data
        context["show_report"] = "show"

        return render(request, "base/import_persons.html", context)

    return render(request, "base/import_persons.html", context)


# handlers
def get_all_files(path):
    return [file for file in os.listdir(path)]


def get_txt_files(path):
    return [file for file in os.listdir(path) if ".txt" in file]


def get_entries(path, files):
    data = ("center", "file", "imported_", "time", "- ")
    entries = []
    for file in files:
        with open(f"{path}/{file}", "r") as _file:
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
    return entries
