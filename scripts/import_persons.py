import csv

from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

from center.models import Center
from user.models import User
from person.models import Historic
from rcadmin.common import short_name


"""
pra rodar via:
./manage.py runscript import_persons --script-args <núcleo> <arquivo_sem_ ext>
O arquivo vai ter que ser copiado para a pasta imports no servidor.
"""


def run(*args):
    # get args
    center_name, file_name = args[0], args[1]
    # get center and file path
    start = timezone.now()
    center = Center.objects.filter(name__icontains=center_name).first()
    file_path = f"../imports/{file_name}.csv"
    report_path = f"../imports/{file_name}_report.txt"
    user = center.made_by
    user_group = Group.objects.get(name="user")
    # lists to report
    importeds, not_email, used_email = [], [], []
    # read file as a dict
    with open(file_path, newline="") as csvfile:
        _dict = csv.DictReader(csvfile)
        for person in _dict:
            if not person.get("email"):
                not_email.append(f"{person['name']}")
            else:
                password = BaseUserManager().make_random_password()

                # creating a new user
                _user = None
                try:
                    new_user = dict(
                        email=person["email"],
                        password=make_password(password),
                    )
                    _user = User.objects.create(**new_user)
                except Exception:
                    used_email.append(f"{person['name']} ({person['email']})")
                if _user:
                    user_group.user_set.add(_user)

                    # updating the user.profile
                    _profile = _user.profile

                    _profile.social_name = short_name(person["name"])
                    _profile.gender = person["gender"]
                    _profile.profession = person["profession"] or ""

                    if person.get("address"):
                        address = person["address"].split(",")
                        _profile.address = str(address[0])
                        try:
                            number_compl = address[1].split("|")  # usar pipe
                            _profile.number = str(number_compl[0].strip())
                            _profile.complement = str(number_compl[1].strip())
                        except Exception:
                            _profile.number = str(address[1].strip())

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
                    _person.reg = person["reg"] or ""
                    _person.name = person["name"]
                    _person.short_name = short_name(person["name"])
                    _person.birth = person["birthday"]
                    _person.observations = f"{person['ps']}" or ""
                    _person.made_by = user

                    # list of aspects
                    aspects = []
                    if person["PRP"]:
                        aspects.append(
                            {"aspect": "PRP", "date": person["PRP"]}
                        )
                    if person["PRB"]:
                        aspects.append(
                            {"aspect": "PRB", "date": person["PRB"]}
                        )
                    if person["PRF"]:
                        aspects.append(
                            {"aspect": "PRF", "date": person["PRF"]}
                        )
                    if person["A1"]:
                        aspects.append({"aspect": "A1", "date": person["A1"]})
                    if person["A2"]:
                        aspects.append({"aspect": "A2", "date": person["A2"]})
                    if person["A3"]:
                        aspects.append({"aspect": "A3", "date": person["A3"]})
                    if person["A4"]:
                        aspects.append({"aspect": "A4", "date": person["A4"]})
                    if person["GR"]:
                        aspects.append({"aspect": "GR", "date": person["GR"]})
                    if person["A5"]:
                        aspects.append({"aspect": "A5", "date": person["A5"]})
                    if person["A6"]:
                        aspects.append({"aspect": "A6", "date": person["A6"]})

                    # last_aspect = max(aspects, key=lambda x: x["date"])
                    _person.aspect = person["aspect"]
                    _person.aspect_date = person["aspect_date"]

                    # updating Aspects
                    if aspects:
                        for aspect in aspects:
                            new_aspect = {
                                "person": _person,
                                "occurrence": aspect["aspect"],
                                "date": aspect["date"],
                                "description": f"on import: {timezone.now()}",
                                "made_by": user,
                            }
                            Historic.objects.create(**new_aspect)

                    # updating Status
                    if person["restriction"] in (
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
                            "description": f"on import in: {timezone.now()}",
                            "made_by": user,
                        }
                        Historic.objects.create(**new_status)
                        _person.status = person["restriction"]

                    _person.save()

                    importeds.append(person["name"])

    # make report
    with open(report_path, "w") as report:
        report.write("#######  IMPORT PERSONS  #######")
        report.write(f"\n\ncenter:     {center}")
        report.write(f"\nfile:       {file_name}.csv")
        report.write(f"\ncreated_by: {user}")
        report.write(f"\nstart:      {start}")
        report.write(f"\nend:        {timezone.now()}")
        report.write("\n\n#######  SUMMARY  #######")
        report.write(f"\n\nIMPORTEDS:  {len(importeds)}")
        report.write(f"\nNOT EMAIL:  {len(not_email)}")
        report.write(f"\nUSED EMAIL: {len(used_email)}")
        report.write("\n\n#######  DETAIL  #######")
        if importeds:
            report.write("\n\nIMPORTEDS:")
            for n, item in enumerate(importeds):
                report.write(f"\n  {n + 1} - {item}")
        if not_email:
            report.write("\n\nNOT EMAIL:")
            for n, item in enumerate(not_email):
                report.write(f"\n  {n + 1} - {item}")
        if used_email:
            report.write("\n\nUSED EMAIL:")
            for n, item in enumerate(used_email):
                report.write(f"\n  {n + 1} - {item}")
