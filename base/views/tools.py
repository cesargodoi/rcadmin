import os
import re
import pandas as pd

from datetime import datetime

from io import StringIO
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, HttpResponse
from django.utils.translation import gettext as _
from django.conf import settings
from center.models import Center
from ..forms import CenterForm

from scripts.import_persons import run as _import_persons


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

        # sanitize and import file
        sanitize_file(IMPORT_PATH, file)

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


# handlers
def get_all_files(path):
    return [file for file in os.listdir(path)]


def get_txt_files(path):
    return [file for file in os.listdir(path) if ".txt" in file]


def get_entries(path, files):
    data = ("center", "file", "imported_", "time", "- ")
    entries = []
    for file in files:
        with open(f"{path}/reports/{file}", "r") as _file:
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


# to pandas
def check_columns(data_frame):
    for column in columns:
        if column not in data_frame.columns:
            return False
    return True


def clear_phone(phone):
    if isinstance(phone, str):
        return "".join(re.findall(r"\d*", phone))
    return phone


def sanitize_file(path, file):
    """sanitize file using pandas"""
    # generate DataFrame
    df = pd.read_csv(
        StringIO(file.read().decode("utf-8")),
        parse_dates=["birthday", "A1", "A2", "A3", "A4", "GR", "A5", "A6"],
    )
    # checking if the file extruture is right
    if not check_columns(df):
        return {"error": "Inconsistent file"}
    # choosing columns that will be used
    df = df[columns]
    # split address
    df[["address", "number", "complement"]] = df["__full_address"].str.split(
        ",", expand=True
    )
    # adjust phones
    df["phone"] = df["phone"].apply(lambda x: clear_phone(x))
    df["cell_phone"] = df["cell_phone"].apply(lambda x: clear_phone(x))
    df["sos_phone"] = df["sos_phone"].apply(lambda x: clear_phone(x))
    # making a new file with records without email
    without_email = df.loc[(df["email"].isnull())]
    without_email_path = f"{path}/without_email/we__{file}"
    without_email.reset_index(drop=True).to_csv(without_email_path)
    # updating the file with records with email
    with_email = df.drop(without_email.index)
    with_email_path = f"{path}/{file}"
    with_email.reset_index(drop=True).to_csv(with_email_path)


columns = [
    "reg",
    "name",
    "gender",
    "birthday",
    "__full_address",
    "district",
    "city",
    "state_prov",
    "zip",
    "country",
    "rg",
    "exp",
    "cpf",
    "phone",
    "cell_phone",
    "email",
    "profession",
    "sos_contact",
    "sos_phone",
    "ps",
    "A1",
    "A2",
    "A3",
    "A4",
    "GR",
    "A5",
    "A6",
]
