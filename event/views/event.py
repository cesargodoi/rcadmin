from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import ACTIVITY_TYPES, clear_session
from base.searchs import search_event

from ..forms import EventForm
from ..models import Event


@login_required
@permission_required("event.view_event")
def event_home(request):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "event/elements/event_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "event/home.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    object_list = None
    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset, page_ = search_event(request, Event)
        object_list = queryset[_from:_to]
        # add action links
        for item in object_list:
            item.click_link = reverse("event_detail", args=[item.pk])

    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "title": _("event home"),
        "type_list": ACTIVITY_TYPES,
        "nav": "home",
    }
    return render(request, template_name, context)


@login_required
@permission_required("event.view_event")
def event_detail(request, pk):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "event/elements/frequency_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "event/detail.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    object = Event.objects.get(pk=pk)
    queryset = object.frequency_set.all().order_by("person__name_sa")
    object_list = queryset[_from:_to]

    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object": object,
        "object_list": object_list,
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
            message = _("The Event has been created!")
            messages.success(request, message)
            return redirect(reverse("event_home") + "?init=on")

    context = {
        "form": EventForm(initial={"made_by": request.user}),
        "form_name": "Event",
        "form_path": "event/forms/event.html",
        "goback": reverse("event_home"),
        "title": _("create event"),
        "to_create": True,
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("event.change_event")
def event_update(request, pk):
    object = Event.objects.get(pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            message = _("The Event has been updated!")
            messages.success(request, message)
            return redirect("event_detail", pk=pk)

    context = {
        "form": EventForm(instance=object),
        "form_name": "Event",
        "form_path": "event/forms/event.html",
        "goback": reverse("event_detail", args=[pk]),
        "title": _("update event"),
        "pk": pk,
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("event.delete_event")
def event_delete(request, pk):
    object = Event.objects.get(pk=pk)
    if object.frequencies.all():
        message = _(
            """
        You cannot delete an event if it has frequencies launched.\n
        Remove all frequencies and try again.
        """
        )
        context = {
            "title": _("action not allowed"),
            "message": message,
        }
        return render(request, "base/action_not_allowed.html", context)

    if request.method == "POST":
        object.delete()
        message = _("The Event has been deleted!")
        messages.success(request, message)
        return redirect(reverse("event_home") + "?init=on")

    context = {
        "object": object,
        "title": _("confirm to delete"),
    }
    return render(request, "base/confirm_delete.html", context)
