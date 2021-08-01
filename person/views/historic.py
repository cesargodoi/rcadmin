from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.utils import timezone
from schooladmin.common import paginator

from ..forms import HistoricForm
from ..models import Historic, Person


@login_required
@permission_required("person.view_historic")
def person_historic(request, person_id):
    queryset = Historic.objects.filter(person=person_id).order_by("-date")
    person = (
        queryset[0].person if queryset else Person.objects.get(id=person_id)
    )

    object_list = paginator(queryset, page=request.GET.get("page"))

    context = {
        "object_list": object_list,
        "title": "historic list",
        "person": person,  # to header element
        "nav": "detail",
        "tab": "historic",
    }
    return render(request, "person/person_detail.html", context)


@login_required
@permission_required("person.add_historic")
def historic_create(request, person_id):
    person = Person.objects.get(id=person_id)
    if request.method == "POST":
        form = HistoricForm(request.POST)
        if form.is_valid():
            form.save()
            adjust_person_side(
                person, request.POST["occurrence"], request.POST["date"]
            )
            messages.success(request, "The Historic has been created!")
        return redirect("person_historic", person_id=person_id)

    context = {
        "form": HistoricForm(
            initial={
                "person": person,
                "made_by": request.user,
                "date": timezone.now(),
            }
        ),
        "title": "create historic",
        "to_create": True,
        "person": person,  # to header element
    }
    return render(request, "person/forms/historic.html", context)


@login_required
@permission_required("person.change_historic")
def historic_update(request, person_id, pk):
    historic = Historic.objects.get(pk=pk)
    if request.method == "POST":
        form = HistoricForm(request.POST, instance=historic)
        if form.is_valid():
            form.save()
            adjust_person_side(
                historic.person,
                request.POST["occurrence"],
                request.POST["date"],
            )
            messages.success(request, "The Historic has been updated!")
        return redirect("person_historic", person_id=person_id)

    context = {
        "form": HistoricForm(instance=historic),
        "title": "update historic",
        "person": historic.person,  # to header element
    }
    return render(request, "person/forms/historic.html", context)


@login_required
@permission_required("person.delete_historic")
def historic_delete(request, person_id, pk):
    historic = Historic.objects.get(pk=pk)
    if request.method == "POST":
        adjust_status_or_aspect(historic)
        historic.delete()
        return redirect("person_historic", person_id=person_id)

    context = {"object": historic, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)


# handlers
def adjust_person_side(person, occurrence, dt):
    date = datetime.strptime(dt, "%Y-%m-%d").date()
    if len(occurrence) == 2:
        if not person.aspect_date or date >= person.aspect_date:
            person.aspect = occurrence
            person.aspect_date = date
            person.save()
    else:
        hist = [
            h.date for h in person.historic_set.all() if len(h.occurrence) == 3
        ]
        hist.sort(reverse=True)
        if date >= hist[0] and occurrence != person.status:
            person.status = occurrence
            person.clean()
            person.save()


def adjust_status_or_aspect(historic):
    date = historic.date
    occurrence = historic.occurrence
    old_historic = [
        (hist.occurrence, hist.date)
        for hist in historic.person.historic_set.all()
    ]
    if len(occurrence) == 2:
        aspect = [asp for asp in old_historic if len(asp[0]) == 2]
        aspect.sort(key=lambda x: x[1], reverse=True)
        if occurrence == aspect[0][0] and date == aspect[0][1]:
            try:
                historic.person.aspect = aspect[1][0]
                historic.person.aspect_date = aspect[1][1]
                historic.person.save()
            except Exception:
                historic.person.aspect = "--"
                historic.person.aspect_date = None
                historic.person.save()
    else:
        status = [stt for stt in old_historic if len(stt[0]) == 3]
        status.sort(key=lambda x: x[1], reverse=True)
        if occurrence == status[0][0] and date == status[0][1]:
            try:
                historic.person.status = status[1][0]
                historic.person.save()
            except Exception:
                historic.person.status = "---"
                historic.person.save()
