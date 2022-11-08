import os
import pandas as pd

from django.conf import settings

from center.models import Center
from person.models import Historic

"""
pra rodar via:
./manage.py runscript people_to_csv --script-args <núcleo>
O arquivo vai ter que ser copiado para a pasta imports no servidor.
"""


def run(*args):
    center = Center.objects.filter(name__icontains=args[0]).first()
    persons = center.person_set.filter(is_active=True)

    to_export = []
    for person in persons:
        _person = {
            "reg": person.reg,
            "name": person.name,
            "birth": person.birth.strftime("%Y-%m-%d"),
            "gender": person.user.profile.gender,
            "id_card": person.id_card,
            "cpf": "",
            "address": person.user.profile.address,
            "number": person.user.profile.number,
            "complement": person.user.profile.complement,
            "district": person.user.profile.district,
            "city": person.user.profile.city,
            "state": person.user.profile.state,
            "country": person.user.profile.country,
            "zip": person.user.profile.zip_code,
            "phone": person.user.profile.phone,
            "cell_phone": person.user.profile.phone,
            "email": person.user.email,
            "sos_contact": person.user.profile.sos_contact,
            "sos_phone": person.user.profile.sos_phone,
            "from": "",
            "to": "",
            "date": "",
            "A1": "",
            "A2": "",
            "A3": "",
            "A4": "",
            "GR": "",
            "A5": "",
            "A6": "",
            "obs": person.observations,
        }

        obs2 = ["*** Other Historic ***"]
        for hist in Historic.objects.filter(person=person):
            if hist.occurrence == "A1":
                _person["A1"] = hist.date.strftime("%Y-%m-%d")
            elif hist.occurrence == "A2":
                _person["A2"] = hist.date.strftime("%Y-%m-%d")
            elif hist.occurrence == "A3":
                _person["A3"] = hist.date.strftime("%Y-%m-%d")
            elif hist.occurrence == "A4":
                _person["A4"] = hist.date.strftime("%Y-%m-%d")
            elif hist.occurrence == "GR":
                _person["GR"] = hist.date.strftime("%Y-%m-%d")
            elif hist.occurrence == "A5":
                _person["A5"] = hist.date.strftime("%Y-%m-%d")
            elif hist.occurrence == "A6":
                _person["A6"] = hist.date.strftime("%Y-%m-%d")

            if len(hist.occurrence) > 2:
                _occurrence = "\r\n- {} - {}".format(
                    hist.date.strftime("%Y-%m-%d"),
                    hist.get_occurrence_display(),
                )
                obs2.append(_occurrence)

        _person["obs2"] = "".join(obs2) if len(obs2) > 1 else ""

        to_export.append(_person)

    # make files
    export_dir = f"{os.path.dirname(settings.BASE_DIR)}/exports"
    csv_file = f"{export_dir}/{center.short_name}_to_CSV.csv"
    pd.DataFrame(to_export).to_csv(csv_file, index=False)
    xlsx_file = f"{export_dir}/{center.short_name}_to_XLSX.xlsx"
    pd.DataFrame(to_export).to_excel(xlsx_file, index=False)
