from django.shortcuts import render

from django.contrib.auth.decorators import login_required, permission_required
from ..models import Person
from center.models import Responsible


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
