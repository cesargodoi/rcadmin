import csv
import os
import pandas as pd

from datetime import datetime

from django.contrib.auth.models import Group
from django.conf import settings

from center.models import Center
from user.models import User
from person.models import Historic
from rcadmin.common import short_name, cpf_validation, cpf_format


"""
pra rodar via:
./manage.py runscript import_persons --script-args <núcleo> <arquivo_sem_ ext>
O arquivo vai ter que ser copiado para a pasta imports no servidor.
"""


def run(*args):
    # get args
    center_name, file_name = args[0], args[1]
    # get center and file path
    start = datetime.now()
    center = Center.objects.filter(name__icontains=center_name).first()
    imports_dir = f"{os.path.dirname(settings.BASE_DIR)}/imports"
    file_path = f"{imports_dir}/{file_name}"
    report_path = (
        f"{imports_dir}/reports/{file_name.split('.')[0]}__report.txt"
    )
    user = center.made_by
    user_group = Group.objects.get(name="user")

    # lists to report
    total, importeds, without_email, used_email = 0, [], [], []

    try:
        with open(
            f"{imports_dir}/without_email/we__{file_name}",
            newline="",
        ) as we:
            _we_dict = csv.DictReader(we)
            for line in _we_dict:
                without_email.append(line["name"])
        total += len(without_email)
    except Exception:
        without_email = []

    # read file as a dict
    with open(file_path, newline="") as csvfile:
        _dict = csv.DictReader(csvfile)
        for person in _dict:
            total += 1
            _user = None
            # creating a new user
            try:
                _user = User.objects.create(email=person["email"])
            except Exception:
                used_email.append(person)

            if _user:
                # add user to group 'user'
                user_group.user_set.add(_user)
                # updating the user.profile
                _profile = _user.profile
                _profile.social_name = short_name(person["name"])
                _profile.gender = person["gender"]
                _profile.profession = person["profession"] or ""
                _profile.address = person["address"]
                _profile.number = person["number"]
                _profile.complement = person["complement"]
                _profile.district = person["district"]
                _profile.city = person["city"]
                _profile.state = person["state_prov"]
                _profile.country = center.country
                _profile.zip_code = person["zip"].strip() or ""
                _profile.phone_1 = person["cell_phone"] or ""
                _profile.phone_2 = person["phone"] or ""
                _profile.sos_contact = person["sos_contact"] or ""
                _profile.sos_phone = person["sos_phone"] or ""
                _profile.save()

                # updating the user.person
                _person = _user.person
                _person.center = center
                _person.reg = person["reg"] if person["reg"] != "0" else ""
                _person.name = person["name"]
                _person.short_name = short_name(person["name"])
                _person.birth = person["birth"]
                _person.observations = f"{person['ps']}" or ""
                _person.made_by = user

                # try register id_card
                if person.get("id_card"):
                    _person.id_card = person["id_card"]
                elif person.get("cpf") and len(person.get("cpf")) >= 11:
                    if cpf_validation(person["cpf"]):
                        _person.id_card = cpf_format(person["cpf"])
                elif person.get("rg"):
                    _person.id_card = (
                        f"{person['rg']} / {person['exp']}"
                        if person.get("exp")
                        else person["rg"]
                    )

                # list of aspects
                aspects = []
                if person.get("PRP"):
                    aspects.append({"aspect": "PRP", "date": person["PRP"]})
                if person.get("PRB"):
                    aspects.append({"aspect": "PRB", "date": person["PRB"]})
                if person.get("PRF"):
                    aspects.append({"aspect": "PRF", "date": person["PRF"]})
                if person.get("A1"):
                    aspects.append({"aspect": "A1", "date": person["A1"]})
                if person.get("A2"):
                    aspects.append({"aspect": "A2", "date": person["A2"]})
                if person.get("A3"):
                    aspects.append({"aspect": "A3", "date": person["A3"]})
                if person.get("A4"):
                    aspects.append({"aspect": "A4", "date": person["A4"]})
                if person.get("GR"):
                    aspects.append({"aspect": "GR", "date": person["GR"]})
                if person.get("A5"):
                    aspects.append({"aspect": "A5", "date": person["A5"]})
                if person.get("A6"):
                    aspects.append({"aspect": "A6", "date": person["A6"]})

                if aspects:
                    # get the last aspect
                    last_aspect = max(aspects, key=lambda x: x["date"])
                    _person.aspect = last_aspect["aspect"]
                    _person.aspect_date = last_aspect["date"]
                    # updating Aspects
                    for aspect in aspects:
                        new_aspect = {
                            "person": _person,
                            "occurrence": aspect["aspect"],
                            "date": aspect["date"],
                            "description": f"on import: {datetime.now()}",
                            "made_by": user,
                        }
                        Historic.objects.create(**new_aspect)

                # updating Status
                if person.get("restriction") in (
                    "ACT",
                    "LIC",
                    "DEA",
                    "DIS",
                    "REM",
                ):
                    new_status = {
                        "person": _person,
                        "occurrence": person["restriction"],
                        "date": person["restriction_date"],
                        "description": f"on import in: {datetime.now()}",
                        "made_by": user,
                    }
                    Historic.objects.create(**new_status)
                    _person.status = person["restriction"]

                _person.save()

                importeds.append(person["name"])

    # write used_email .csv file
    if used_email:
        pd.DataFrame(used_email).to_csv(
            f"{imports_dir}/used_email/ue__{file_name}",
            encoding="utf-8",
            index=False,
        )

    # make report
    with open(report_path, "w") as report:
        report.write("  IMPORT PERSONS  ".center(80, "*"))
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
        report.write(f"\n- IMPORTEDS:       {len(importeds)}")
        report.write(f"\n- WITHOUT_EMAIL:   {len(without_email)}")
        report.write(f"\n- USED_EMAIL:      {len(used_email)}")
        report.write("\n\n")
        report.write("  DETAIL  ".center(80, "*"))
        if importeds:
            report.write("\n\nIMPORTEDS:")
            for n, item in enumerate(importeds):
                report.write(f"\n  {n + 1} - {item}")
        if without_email:
            report.write("\n\nWITHOUT EMAIL:")
            for n, item in enumerate(without_email):
                report.write(f"\n  {n + 1} - {item}")
        if used_email:
            report.write("\n\nUSED_EMAIL:")
            for n, item in enumerate(used_email):
                report.write(f"\n  {n + 1} - {item['name']}")
