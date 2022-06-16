from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from event.models import Event
from base.searchs import search_event
from rcadmin.common import (
    ACTIVITY_TYPES,
    clear_session,
    get_template_and_pagination,
)

from ..models import Person


@login_required
@permission_required("event.view_event")
def frequency_ps_list(request, person_id):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request, "person/detail.html", "person/elements/frequency_list.html"
    )

    person = Person.objects.get(id=person_id)
    queryset = person.frequency_set.all().order_by("-event__date")
    count = len(queryset)
    object_list = queryset[_from:_to]
    # add action links
    for item in object_list:
        item.del_link = reverse(
            "frequency_ps_delete", args=[person_id, item.event.id]
        )

    if not request.htmx and object_list:
        message = f"{count} records were found in the database"
        messages.success(request, message)

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "title": _("frequencies list"),
        "object": person,  # to header element,
        "nav": "detail",
        "tab": "frequencies",
    }
    return render(request, template_name, context)


@login_required
@permission_required("person.change_person")
def frequency_ps_insert(request, person_id):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "person/frequency_insert.html",
        "person/elements/event_list.html",
    )

    person = Person.objects.get(id=person_id)

    if request.GET.get("pk"):
        event = Event.objects.get(pk=request.GET.get("pk"))

        if request.method == "POST":
            person.frequency_set.create(
                person=person,
                event=event,
                aspect=person.aspect,
            )
            messages.success(request, "The Frequency has been inserted!")
            return redirect("frequency_ps_list", person_id=person_id)

        context = {
            "object": "{} ➜ {} - {}".format(
                person.name, event.activity.name, event.center
            ),
            "confirm_link": "{}?pk={}".format(
                reverse("frequency_ps_insert", args=[person_id]),
                request.GET.get("pk"),
            ),
        }
        return render(request, "person/confirm/insert.html", context)

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_event(request, Event, _from, _to)
        # add action links
        for member in object_list:
            member.add_link = reverse("frequency_ps_insert", args=[person_id])

    if not request.htmx and object_list:
        message = f"{count} records were found in the database"
        messages.success(request, message)

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "init": True if request.GET.get("init") else False,
        "title": _("insert frequencies"),
        "type_list": ACTIVITY_TYPES,
        "pre_freqs": [
            person.event.pk for person in person.frequency_set.all()
        ],
        "person_id": person_id,  # to goback
    }
    return render(request, template_name, context)


@require_http_methods(["GET", "DELETE"])
@login_required
@permission_required("person.change_person")
def frequency_ps_delete(request, person_id, event_id):
    person = Person.objects.get(id=person_id)
    event = Event.objects.get(pk=event_id)

    if request.method == "DELETE":
        person.event_set.remove(event)
        return redirect("frequency_ps_list", person_id=person_id)

    template_name = "person/confirm/delete.html"
    context = {
        "object": "{} ⛔️ {} - {}".format(
            person.name, event.activity.name, event.center
        ),
        "del_link": reverse("frequency_ps_delete", args=[person_id, event_id]),
        "target": "#frequencyList",
    }
    return render(request, template_name, context)
