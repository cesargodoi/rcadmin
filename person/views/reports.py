import pandas as pd

# from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import gettext as _
from django.urls import reverse

from ..models import Person
from center.models import Responsible
from base.utils import get_person_dict


@login_required
@permission_required("person.view_person")
def person_badge(request, person_id):
    template = "person/reports/person_badge.html"
    person = Person.objects.get(id=person_id)
    responsibles = Responsible.objects.filter(center=person.center, rule="BDG")

    context = {
        "person": person,
        "responsibles": responsibles,
    }
    return render(request, template, context)


@login_required
@permission_required("publicwork.view_lecture")
def installed_per_period(request):
    if request.GET.get("dt1") and request.GET.get("dt2"):
        # get person dict
        _dict = get_person_dict(request, Person)
        if _dict:
            # select columns to report
            columns = [
                "name",
                "local",
                "status",
                "aspect",
                "date",
            ]
            # generate pandas dataframe
            report_data = pd.DataFrame(_dict, columns=columns)
            #  adjust index
            report_data.index += 1

            context = {
                "title": _("installed per period"),
                "subtitle": request.user.person.center,
                "report_data": report_data.to_html(),
                "goback": reverse("person_home") + "?init=on",
                "search": "base/searchs/modal_period.html",
            }

            return render(request, "base/reports/show_report.html", context)

    context = {
        "title": _("installed per period"),
        "goback": reverse("person_home") + "?init=on",
        "search": "base/searchs/modal_period.html",
    }

    return render(request, "base/reports/show_report.html", context)
