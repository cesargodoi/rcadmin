import csv
import os
import json
import pandas as pd

from datetime import datetime

from django.conf import settings
from django.urls import reverse

from center.models import Center
from person.models import Invitation
from user.models import User
from rcadmin.common import cpf_validation, cpf_format, sanitize_name


"""
pra rodar via:
./manage.py runscript import_persons --script-args <núcleo> <arquivo_sem_ext>
O arquivo vai ter que ser copiado para a pasta imports no servidor.
"""


def run(*args):
    # get args
    center_name, file_name = args[0], args[1]

    # get center and file path
    start = datetime.now()
    center = Center.objects.filter(name__icontains=center_name).first()
    import_dir = f"{os.path.dirname(settings.BASE_DIR)}/imports"
    file_path = f"{import_dir}/{file_name}.csv"
    report_path = f"{import_dir}/reports/{file_name}__report.txt"
    user = center.made_by

    # lists to report
    total = 0
    importeds = []
    without_email = []
    duplicate_email = []
    used_email = []
    to_send_email = []

    try:
        with open(
            f"{import_dir}/without_email/without_email__{file_name}.csv",
            newline="",
        ) as we:
            _we_dict = csv.DictReader(we)
            for line in _we_dict:
                without_email.append(line["name"])
        total += len(without_email)
    except Exception:
        without_email = []

    try:
        with open(
            f"{import_dir}/duplicate_email/duplicate_email__{file_name}.csv",
            newline="",
        ) as de:
            _de_dict = csv.DictReader(de)
            for line in _de_dict:
                duplicate_email.append(f"{line['name']} - {line['email']}")
        total += len(duplicate_email)
    except Exception:
        duplicate_email = []

    # read file as a dict
    with open(file_path, newline="") as csvfile:
        _dict = csv.DictReader(csvfile)
        for row in _dict:
            total += 1
            # new invite
            _invite = None
            # checking if email exists in User database
            if User.objects.filter(email=row["email"]):
                used_email.append(row)
            else:
                try:
                    # try to create new invite
                    _invite = Invitation.objects.create(
                        center=center,
                        name=sanitize_name(row["name"]),
                        email=row["email"],
                        migration=True,
                    )
                    importeds.append(
                        f"{sanitize_name(row['name'])} - {row['email']}"
                    )
                except Exception:
                    used_email.append(row)

            if _invite:
                _invite.birth = row["birth"]
                _invite.gender = row["gender"]
                _invite.address = row["address"]
                _invite.number = row["number"]
                _invite.complement = row["complement"]
                _invite.district = row["district"]
                _invite.city = row["city"]
                _invite.state = row["state"]
                _invite.country = center.country
                _invite.zip_code = row["zip"].strip() or ""
                _invite.phone = (
                    row["cell_phone"].strip() or row["phone"].strip()
                )
                _invite.sos_contact = sanitize_name(row["sos_contact"]) or ""
                _invite.sos_phone = row["sos_phone"].strip()
                _invite.made_by = user

                # try register id_card
                if row.get("id_card") and len(row.get("id_card")) > 3:
                    _invite.id_card = row["id_card"]
                if row.get("cpf") and len(row.get("cpf")) >= 11:
                    if cpf_validation(row["cpf"]):
                        _invite.id_card = cpf_format(row["cpf"])

                # list of occurrences
                occurrences = {}
                if row.get("A1"):
                    occurrences["A1"] = row["A1"]
                if row.get("A2"):
                    occurrences["A2"] = row["A2"]
                if row.get("A3"):
                    occurrences["A3"] = row["A3"]
                if row.get("A4"):
                    occurrences["A4"] = row["A4"]
                if row.get("GR"):
                    occurrences["GR"] = row["GR"]
                if row.get("A5"):
                    occurrences["A5"] = row["A5"]
                if row.get("A6"):
                    occurrences["A6"] = row["A6"]

                # observations
                if row.get("obs"):
                    _invite.observations = f"| {row['obs']} "
                if row.get("obs2"):
                    _invite.observations += f"| {row['obs2']} "

                # import retrog
                if row.get("from"):
                    _invite.observations += "| Retrog. {} -> {} in {} ".format(
                        row["from"], row["to"], row["date"]
                    )

                _invite.historic = json.loads(json.dumps(occurrences))

                _invite.save()

                # to send email
                to_send = {
                    "name": _invite.name,
                    "email": _invite.email,
                    "link": "{}{}".format(
                        "https://rcadmin.rosacruzaurea.org.br",
                        reverse("confirm_invitation", args=[_invite.pk]),
                    ),
                }
                to_send_email.append(to_send)

    # write used_email .csv file
    if used_email:
        pd.DataFrame(used_email).to_csv(
            f"{import_dir}/used_email/used_email__{file_name}.csv",
            encoding="utf-8",
            index=False,
        )

    # write to_send_email .csv file
    if to_send_email:
        pd.DataFrame(to_send_email).to_csv(
            f"{import_dir}/to_send_email/to_send_email__{file_name}.csv",
            encoding="utf-8",
            index=False,
        )

    # make report
    with open(report_path, "w") as report:
        report.write("  IMPORT PEOPLE  ".center(80, "*"))
        report.write(f"\n\ncenter:      {center}")
        report.write(f"\nfile:        {file_name}.csv")
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
        report.write(f"\n- DUPLICATE_EMAIL: {len(duplicate_email)}")
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
        if duplicate_email:
            report.write("\n\nDUPLICATE EMAIL:")
            for n, item in enumerate(duplicate_email):
                report.write(f"\n  {n + 1} - {item}")
        if used_email:
            report.write("\n\nUSED_EMAIL:")
            for n, item in enumerate(used_email):
                _item = f"{sanitize_name(item['name'])} - {item['email']}"
                report.write(f"\n  {n + 1} - {_item}")
