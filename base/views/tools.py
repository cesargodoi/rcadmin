import csv
from io import StringIO
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.contrib import messages
from center.models import Center
from user.models import User
from person.models import Historic
from ..forms import CenterForm
from schooladmin.common import short_name


@user_passes_test(lambda u: u.is_superuser)
def import_persons(request):
    if request.method == "POST":
        center = Center.objects.get(id=request.POST.get("conf_center"))
        user = request.user
        user_group = Group.objects.get(name="user")

        _file = request.FILES.get("import_file")
        _dict = csv.DictReader(StringIO(_file.read().decode("utf-8")))

        importeds, no_email, used_email = [], [], []
        for person in _dict:
            if not person.get("email"):
                no_email.append(f"{person['name']}")
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
                    _profile.profession = person["profession"]

                    if person.get("address"):
                        address = person["address"].split(",")
                        _profile.address = str(address[0])
                        try:
                            number_compl = address[1].split("-")
                            _profile.number = str(number_compl[0].strip())
                            _profile.complement = str(number_compl[1].strip())
                        except Exception:
                            _profile.number = str(address[1].strip())

                    _profile.disctrict = person["district"]
                    _profile.city = person["city"]
                    _profile.state = person["state_prov"]
                    _profile.country = center.country
                    _profile.zip_code = person["zip"].strip()
                    _profile.phone_1 = person["cell_phone"]
                    _profile.phone_2 = person["phone"]
                    _profile.sos_contact = person["sos_contact"]
                    _profile.sos_phone = person["sos_phone"]

                    _profile.save()

                    # updating the user.person
                    _person = _user.person

                    _person.center = center
                    _person.reg = person[
                        "reg"
                    ]  # need to confirm with presidium
                    _person.name = person["name"]
                    _person.short_name = short_name(person["name"])
                    _person.birth = person["birthday"]
                    _person.observations = (
                        f"first password: {password}\n{person['ps']}"
                    )
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

        report_data = dict(
            center=center,
            user=user,
            date=timezone.now(),
            importeds=importeds,
            no_email=no_email,
            used_email=used_email,
            total=len(importeds) + len(no_email) + len(used_email),
            file=_file.name,
        )

        message = f"{len(importeds)} Persons has been imported!"
        messages.success(request, message)
        context = {
            "title": "import persons",
            "form": CenterForm(),
            "report_data": report_data,
            "search": "base/searchs/modal_import_persons.html",
        }
        return render(request, "base/import_persons.html", context)

    context = {
        "title": "import persons",
        "form": CenterForm(),
        "search": "base/searchs/modal_import_persons.html",
    }
    return render(request, "base/import_persons.html", context)
