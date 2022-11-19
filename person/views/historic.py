from datetime import datetime

from django.http import QueryDict
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from rcadmin.common import get_template_and_pagination
from ..forms import HistoricForm
from ..models import Historic, Person


@login_required
@permission_required("person.view_historic")
def person_historic(request, person_id):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request, "person/detail.html", "person/elements/historic_list.html"
    )

    queryset = Historic.objects.filter(person=person_id).order_by("-date")
    person = (
        queryset[0].person if queryset else Person.objects.get(id=person_id)
    )

    count = len(queryset)
    object_list = queryset[_from:_to]

    # add action links
    for item in object_list:
        item.update_link = reverse(
            "historic_update", args=[person_id, item.pk]
        )
        item.del_link = reverse("historic_delete", args=[person_id, item.pk])

    if not request.htmx and object_list:
        message = f"{count} records were found in the database"
        messages.success(request, message)

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "title": _("historic list"),
        "object": person,  # to header element
        "nav": "detail",
        "tab": "historic",
    }
    return render(request, template_name, context)


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

    template_name = "person/forms/historic.html"
    context = {
        "title": _("Create historic"),
        "form": HistoricForm(
            initial={
                "person": person,
                "made_by": request.user,
                "date": timezone.now(),
            }
        ),
        "callback_link": reverse("historic_create", args=[person_id]),
        "person_id": person_id,  # to header element
    }
    return render(request, template_name, context)


@login_required
@permission_required("person.change_historic")
def historic_update(request, person_id, pk):
    historic = Historic.objects.get(pk=pk)

    if request.method == "POST":
        data = QueryDict(request.body).dict()
        form = HistoricForm(data, instance=historic)
        if form.is_valid():
            form.save()
            adjust_person_side(
                historic.person,
                request.POST["occurrence"],
                request.POST["date"],
            )

            historic.update_link = reverse(
                "historic_update", args=[person_id, pk]
            )
            historic.del_link = reverse(
                "historic_delete", args=[person_id, pk]
            )

            template_name = "person/elements/hx/historic_updated.html"
            context = {"obj": historic, "pos": request.GET.get("pos")}
            return render(request, template_name, context)

    template_name = "person/forms/historic.html"
    context = {
        "title": _("Update Historic"),
        "form": HistoricForm(instance=historic),
        "callback_link": reverse("historic_update", args=[person_id, pk]),
        "target": f"HST{pk}",
        "swap": "innerHTML",
        "pos": request.GET.get("pos"),
        "update": True,
    }
    return render(request, template_name, context)


@require_http_methods(["GET", "DELETE"])
@login_required
@permission_required("person.delete_historic")
def historic_delete(request, person_id, pk):
    historic = Historic.objects.get(pk=pk)

    if request.method == "DELETE":
        adjust_status_or_aspect(historic)
        historic.delete()
        return redirect("person_historic", person_id=person_id)

    template_name = "person/confirm/delete.html"
    context = {
        "object": historic,
        "del_link": reverse("historic_delete", args=[person_id, pk]),
        "target": "#historicList",
    }
    return render(request, template_name, context)


# handlers
def adjust_person_side(person, occurrence, dt):
    if isinstance(dt, str):
        date = datetime.strptime(dt, "%Y-%m-%d").date()
    else:
        date = dt
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
