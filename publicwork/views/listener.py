from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from rcadmin.common import (
    clear_session,
    SEEKER_STATUS,
    LECTURE_TYPES,
)
from django.urls import reverse

from center.models import Center
from base.searchs import search_seeker, search_lecture

from ..forms import ListenerForm
from ..models import Lecture, Seeker, Listener


@login_required
@permission_required("publicwork.add_listener")
def add_listener(request, lect_pk):
    # set limit of registers
    LIMIT = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "publicwork/listener/elements/seeker_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "publicwork/listener/add.html"
        page = 1
    # get limitby
    _from, _to = LIMIT * (page - 1), LIMIT * page

    object_list = None
    lecture = Lecture.objects.get(pk=lect_pk)

    if request.GET.get("seek_pk"):
        seeker = Seeker.objects.get(pk=request.GET["seek_pk"])

        if request.method == "POST":
            # create listener
            Listener.objects.create(
                lecture=lecture,
                seeker=seeker,
                ranking=int(request.POST["ranking"]),
                observations=request.POST["observations"],
            )
            messages.success(
                request, _("The seeker has been inserted on lecture!")
            )
            return redirect("lecture_detail", pk=lect_pk)

        context = {
            "seeker": seeker,
            "form": ListenerForm,
            "insert_to": f"{lecture.theme} {lecture.center}",
            "title": _("confirm to insert"),
        }
        return render(
            request,
            "publicwork/listener/confirm.html",
            context,
        )

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        queryset, count = search_seeker(request, Seeker, _from, _to)
        object_list = queryset[_from:_to]
        # add action links
        for item in object_list:
            item.add_link = reverse("add_listener", args=[lect_pk])
            item.local = f"{item.city} ({item.state}-{item.country})"

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("add_listener", args=[lecture.pk]),
        "status_list": SEEKER_STATUS,
        "pre_listeners": [seek.pk for seek in lecture.listeners.all()],
        "title": _("add listener"),
        "object": lecture,
        "centers": [[str(cnt.pk), str(cnt)] for cnt in Center.objects.all()],
        "user_center": str(request.user.person.center.pk),
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.change_listener")
def update_listener(request, lect_pk, lstn_pk):
    listener = Listener.objects.get(pk=lstn_pk)

    if request.method == "POST":
        listener.ranking = int(request.POST["ranking"])
        listener.observations = request.POST["observations"]
        listener.save()
        messages.success(request, _("The Listener has been updated!"))

        return redirect("lecture_detail", pk=lect_pk)

    context = {
        "form": ListenerForm(instance=listener),
        "title": _("update listener"),
        "listener": listener,
        "object": listener.lecture,
    }
    return render(request, "publicwork/listener/update.html", context)


@login_required
@permission_required("publicwork.delete_listener")
def remove_listener(request, lect_pk, lstn_pk):
    listener = Listener.objects.get(pk=lstn_pk)

    if request.method == "POST":
        listener.delete()
        return redirect("lecture_detail", pk=lect_pk)

    context = {
        "object": listener,
        "title": _("confirm to delete"),
    }
    return render(request, "base/confirm_delete.html", context)


# from seeker side  ###########################################################
@login_required
@permission_required("publicwork.add_listener")
def add_frequency(request, pk):
    # set limit of registers
    LIMIT = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "publicwork/listener/elements/lecture_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "publicwork/seeker/add_or_change.html"
        page = 1
    # get limitby
    _from, _to = LIMIT * (page - 1), LIMIT * page

    seeker = Seeker.objects.get(pk=pk)

    if request.GET.get("lect_pk"):
        lecture = Lecture.objects.get(pk=request.GET["lect_pk"])

        if request.method == "POST":
            # create listener
            Listener.objects.create(
                lecture=lecture,
                seeker=seeker,
                ranking=int(request.POST["ranking"]),
                observations=request.POST["observations"],
            )
            messages.success(
                request, _("The seeker has been inserted on lecture!")
            )
            return redirect("seeker_frequencies", pk=pk)

        context = {
            "seeker": seeker,
            "form": ListenerForm,
            "insert_to": f"{lecture.theme} - {lecture.center}",
            "title": _("confirm to insert"),
        }
        return render(
            request,
            "publicwork/listener/confirm.html",
            context,
        )

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_lecture(request, Lecture, _from, _to)
        # add action links
        for item in object_list:
            item.add_link = reverse("add_frequency", args=[pk])

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object": seeker,
        "object_list": object_list,
        "count": count,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("seeker_home"),
        "title": _("add frequency"),
        "type_list": LECTURE_TYPES,
        "pre_freqs": [lect.pk for lect in seeker.lecture_set.all()],
        "tab": "frequencies",
        "add": True,
        "goback": reverse("seeker_frequencies", args=[pk]),
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.change_listener")
def update_frequency(request, seek_pk, freq_pk):
    seeker = Seeker.objects.get(pk=seek_pk)
    listener = Listener.objects.get(pk=freq_pk)
    if request.method == "POST":
        listener.ranking = (
            int(request.POST["ranking"]) if request.POST.get("ranking") else 0
        )
        listener.observations = request.POST["observations"]
        listener.save()
        messages.success(request, _("The Listener has been updated!"))
        return redirect("seeker_frequencies", pk=seek_pk)

    context = {
        "object": seeker,
        "listener": listener,
        "form": ListenerForm(instance=listener),
        "title": _("update frequency | seeker side"),
        "seeker_side": True,
        "goback": reverse("seeker_frequencies", args=[seek_pk]),
    }
    return render(request, "publicwork/listener/update.html", context)


@login_required
@permission_required("publicwork.delete_listener")
def remove_frequency(request, seek_pk, freq_pk):
    listener = Listener.objects.get(pk=freq_pk)

    if request.method == "POST":
        listener.delete()
        return redirect("seeker_frequencies", pk=seek_pk)

    context = {
        "object": listener,
        "title": _("confirm to delete"),
    }
    return render(request, "base/confirm_delete.html", context)
