from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from event.models import Event
from base.searchs import search_event
from rcadmin.common import ACTIVITY_TYPES, clear_session

from ..models import Person


@login_required
@permission_required("event.view_event")
def frequency_ps_list(request, person_id):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "person/elements/frequency_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "person/detail.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    person = Person.objects.get(id=person_id)
    queryset = person.frequency_set.all().order_by("-event__date")
    object_list = queryset[_from:_to]

    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object_list": object_list,
        "title": _("frequencies list"),
        "object": person,  # to header element,
        "nav": "detail",
        "tab": "frequencies",
    }
    return render(request, template_name, context)


@login_required
@permission_required("person.change_person")
def frequency_ps_insert(request, person_id):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "person/elements/event_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "person/frequency_insert.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    object_list = None
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
            "person": person,
            "insert_to": f"{event.activity.name} {event.center}",
            "title": _("confirm to insert"),
        }
        return render(
            request, "person/elements/confirm_to_insert.html", context
        )

    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset = search_event(request, Event)
        object_list = queryset[_from:_to]
        # add action links
        for member in object_list:
            member.add_link = reverse("frequency_ps_insert", args=[person_id])

    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "title": _("insert frequencies"),
        "type_list": ACTIVITY_TYPES,
        "pre_freqs": [
            person.event.pk for person in person.frequency_set.all()
        ],
        "person_id": person_id,  # to goback
    }
    return render(request, template_name, context)


@login_required
@permission_required("person.change_person")
def frequency_ps_delete(request, person_id, event_id):
    person = Person.objects.get(id=person_id)
    event = Event.objects.get(pk=event_id)
    if request.method == "POST":
        person.event_set.remove(event)
        messages.success(request, "The Frequency has been removed!")
        return redirect("frequency_ps_list", person_id=person_id)

    context = {
        "person": person,
        "event": event,
        "title": _("confirm to delete"),
    }
    return render(
        request, "person/elements/confirm_to_delete_freq.html", context
    )
