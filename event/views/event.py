from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import (
    ACTIVITY_TYPES,
    clear_session,
    get_template_and_pagination,
)
from base.searchs import search_event

from ..forms import EventForm
from ..models import Event


@login_required
@permission_required("event.view_event")
def event_home(request):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request, "event/home.html", "event/elements/event_list.html"
    )

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_event(request, Event, _from, _to)
        # add action links
        for item in object_list:
            item.click_link = reverse("event_detail", args=[item.pk])

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
        "title": _("event home"),
        "type_list": ACTIVITY_TYPES,
        "nav": "home",
    }
    return render(request, template_name, context)


@login_required
@permission_required("event.view_event")
def event_detail(request, pk):
    object = Event.objects.get(pk=pk)

    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request, "event/detail.html", "event/elements/frequency_list.html"
    )

    _object_list = object.frequency_set.all().order_by("person__name_sa")
    count = len(_object_list)
    object_list = _object_list[_from:_to]

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": object,
        "title": _("event detail"),
        "nav": "detail",
    }
    return render(request, template_name, context)


@login_required
@permission_required("event.add_event")
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()

        LIMIT, template_name, _from, _to, page = get_template_and_pagination(
            request, "event/home.html", "event/elements/event_list.html"
        )
        object_list, count = search_event(request, Event, _from, _to)
        # add action links
        for item in object_list:
            item.click_link = reverse("event_detail", args=[item.pk])

        template_name = "event/elements/event_list.html"
        context = {
            "LIMIT": LIMIT,
            "page": page,
            "counter": (page - 1) * LIMIT,
            "object_list": object_list,
            "count": count,
        }
        return render(request, template_name, context)

    template_name = "event/forms/event.html"
    context = {
        "title": _("Create historic"),
        "form": EventForm(initial={"made_by": request.user}),
        "callback_link": reverse("event_create"),
        "target": "eventList",
        "swap": "innerHTML",
    }
    return render(request, template_name, context)


@login_required
@permission_required("event.change_event")
def event_update(request, pk):
    obj = Event.objects.get(pk=pk)

    if request.method == "POST":
        form = EventForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()

        return render(request, "event/header.html", {"object": obj})

    print()
    template_name = "event/forms/event.html"
    context = {
        "title": _("update event"),
        "form": EventForm(instance=obj),
        "callback_link": reverse("event_update", args=[pk]),
        "target": "eventHeader",
        "swap": "innerHTML",
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("event.delete_event")
def event_delete(request, pk):
    template_name = "event/confirm/delete.html"
    event = Event.objects.get(pk=pk)

    if event.frequencies.all():
        message = _(
            """
        You cannot delete an event if it has frequencies launched.\n
        Remove all frequencies and try again.
        """
        )
        context = {
            "allowed": False,
            "object": message,
        }
        return render(request, template_name, context)

    if request.method == "POST":
        event.delete()
        return redirect("event_home")

    context = {
        "allowed": True,
        "object": event,
        "del_link": reverse("event_delete", args=[pk]),
    }
    return render(request, template_name, context)
