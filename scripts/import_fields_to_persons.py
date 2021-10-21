import csv
import os

from datetime import datetime
from dateutil.parser import parse

from django.conf import settings

from center.models import Center
from person.models import Person
from rcadmin.common import (
    cpf_validation,
    cpf_format,
    DEFAULT_DATES,
)


"""
pra rodar via:
./manage.py runscript import_fields_to_persons --script-args <núcleo> 
                                                             <arquivo_sem_ext>
O arquivo vai ter que ser copiado para a pasta imports no servidor.
"""


def run(*args):
    # get args
    center_name, file_name = args[0], args[1]
    # get center and file path
    start = datetime.now()
    center = Center.objects.filter(name__icontains=center_name).first()
    user = center.made_by
    imports_dir = f"{os.path.dirname(settings.BASE_DIR)}/imports"
    file_path = f"{imports_dir}/fields__{file_name}"
    report_path = (
        f"{imports_dir}/reports/fields/{file_name.split('.')[0]}__report.txt"
    )

    # to report
    fields, total, adjusteds = [], 0, []

    # get fields
    with open(file_path, "r") as csvfile:
        fields = [
            f.replace("\n", "")
            for f in csvfile.readline().split(",")
            if f not in ("", "name")
        ]

    # read file as a dict
    with open(file_path, newline="") as csvfile:
        _dict = csv.DictReader(csvfile)
        for _person in _dict:
            person = Person.objects.filter(
                center=center, name__icontains=_person.get("name")
            ).first()
            if person:
                total += 1
                alter = 0
                for attr in fields:
                    # try register id_card
                    if attr == "rg":
                        id_card = (
                            f"{_person['rg']} / {_person['exp']}"
                            if _person.get("exp")
                            else _person["rg"]
                        )
                        if person.id_card != id_card:
                            person.__setattr__("id_card", id_card)
                            alter += 1
                    elif attr == "cpf" and len(_person[attr]) >= 11:
                        if cpf_validation(_person[attr]):
                            if person.id_card != cpf_format(_person[attr]):
                                person.__setattr__(
                                    "id_card", cpf_format(_person[attr])
                                )
                                alter += 1

                    elif attr != "exp":
                        # register dates
                        if attr in DEFAULT_DATES:
                            if (
                                person.__getattribute__(attr)
                                != parse(_person[attr]).date()
                            ):
                                person.__setattr__(attr, _person[attr])
                                alter += 1
                        # register other fields
                        elif person.__getattribute__(attr) != _person[attr]:
                            person.__setattr__(attr, _person[attr])
                            alter += 1
                if alter > 0:
                    adjusteds.append(person.short_name)
                    person.save()

    # make report
    with open(report_path, "w") as report:
        report.write("  ADJUSTED FIELDS ON PERSON  ".center(80, "*"))
        report.write(f"\n\ncenter:      {center}")
        report.write(f"\nfile:        {file_name}")
        report.write(f"\nimported_by: {user}")
        report.write(
            f"\nimported_on: {start.strftime('%Y-%m-%d %H:%M:%S.%f')}"
        )
        report.write(f"\ntime:        {datetime.now() - start}")
        report.write("\n\n")
        report.write("  SUMMARY  ".center(80, "*"))
        report.write(f"\n\n- ENTRIES:         {total}")
        report.write(f"\n- FIELDS:          {','.join(fields)}")
        report.write(f"\n- ADJUSTEDS:       {len(adjusteds)}")
        report.write("\n\n")
        report.write("  DETAIL  ".center(80, "*"))
        if adjusteds:
            report.write("\n\nADJUSTEDS:")
            for n, item in enumerate(adjusteds):
                report.write(f"\n  {n + 1} - {item}")
