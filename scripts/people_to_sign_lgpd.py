import os
import pandas as pd

from datetime import datetime

from django.conf import settings
from django.urls import reverse

from center.models import Center
from person.models import Invitation
from rcadmin.common import sanitize_name

"""
pra rodar via:
./manage.py runscript people_to_sign_lgpd --script-args <núcleo>
O arquivo vai ter que ser copiado para a pasta imports no servidor.
"""


def run(*args):
    start = datetime.now()
    # get vars
    center = Center.objects.filter(name__icontains=args[0]).first()
    persons = center.person_set.filter(is_active=True)

    # get path to reports
    import_dir = f"{os.path.dirname(settings.BASE_DIR)}/imports"
    report_path = "{}/reports/{}_to_sign_lgpd__report.txt".format(
        import_dir, args[0]
    )
    user = center.made_by

    # lists to report
    people_to_sign_lgpd = []
    to_send_email = []

    count = 1
    for person in persons:
        invite = {
            "center": center,
            "name": person.name,
            "birth": person.birth,
            "gender": person.user.profile.gender,
            "id_card": person.id_card,
            "address": person.user.profile.address,
            "number": person.user.profile.number,
            "complement": person.user.profile.complement,
            "district": person.user.profile.district,
            "city": person.user.profile.city,
            "state": person.user.profile.state,
            "country": person.user.profile.country,
            "zip_code": person.user.profile.zip_code,
            "phone": person.user.profile.phone,
            "email": person.user.email,
            "sos_contact": person.user.profile.sos_contact,
            "sos_phone": person.user.profile.sos_phone,
            "historic": {str(person.aspect): str(person.aspect)},
            "observations": person.observations,
            "migration": True,
            "sign_lgpd": True,
        }

        # TODO - cuidar de que o fluxo não quebre (try except)
        new = Invitation.objects.create(**invite)

        person.is_active = False
        person.user.is_active = False
        person.save()

        # to report
        people_to_sign_lgpd.append(f"{sanitize_name(new.name)} - {new.email}")

        # to send email
        to_send = {
            "name": new.name,
            "email": new.email,
            "link": "{}{}".format(
                "https://rcadmin.rosacruzaurea.org.br",
                reverse("confirm_invitation", args=[new.pk]),
            ),
        }
        to_send_email.append(to_send)

        print(f"{count} -> {person}")
        count += 1
    
    # write to_send_email .csv file
    if to_send_email:
        pd.DataFrame(to_send_email).to_csv(
            "{}/to_send_email/to_send_email__{}__to_sign_lgpd.csv".format(
                import_dir,
                args[0],
            ),
            encoding="utf-8",
            index=False,
        )

    # import report
    with open(report_path, "w") as report:
        report.write("  PEOPLE TO SIGN LGPD  ".center(80, "*"))
        report.write(f"\n\ncenter:      {center}")
        report.write(f"\nimported_by: {user}")
        report.write(
            f"\nimported_on: {start.strftime('%Y-%m-%d %H:%M:%S.%f')}"
        )
        report.write(f"\ntime:        {datetime.now() - start}")
        report.write("\n\n")
        report.write("  SUMMARY  ".center(80, "*"))
        report.write(f"\n\n- IMPORTEDS:       {len(people_to_sign_lgpd)}")
        report.write("\n\n")
        report.write("  DETAIL  ".center(80, "*"))
        if people_to_sign_lgpd:
            report.write("\n\nIMPORTEDS:")
            for n, item in enumerate(people_to_sign_lgpd):
                report.write(f"\n  {n + 1} - {item}")
