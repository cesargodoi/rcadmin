from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from schooladmin.common import (
    paginator,
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
                request, "The seeker has been inserted on lecture!"
            )
            return redirect("lecture_detail", pk=lect_pk)

        context = {
            "seeker": seeker,
            "form": ListenerForm,
            "insert_to": f"{lecture.theme} {lecture.center}",
            "title": "confirm to insert",
        }
        return render(
            request,
            "publicwork/elements/confirm_add_listener.html",
            context,
        )

    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset, page = search_seeker(request, Seeker)
        object_list = paginator(queryset, page=page)
        # add action links
        for item in object_list:
            item.add_link = reverse("add_listener", args=[lect_pk])

    context = {
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("add_listener", args=[lecture.pk]),
        "status_list": SEEKER_STATUS,
        "pre_listeners": [seek.pk for seek in lecture.listeners.all()],
        "title": "add listener",
        "object": lecture,
        "centers": [[str(cnt.pk), str(cnt)] for cnt in Center.objects.all()],
    }
    return render(request, "publicwork/listener_add.html", context)


@login_required
@permission_required("publicwork.change_listener")
def update_listener(request, lect_pk, lstn_pk):
    listener = Listener.objects.get(pk=lstn_pk)

    if request.method == "POST":
        listener.ranking = int(request.POST["ranking"])
        listener.observations = request.POST["observations"]
        listener.save()
        messages.success(request, "The Listener has been updated!")

        return redirect("lecture_detail", pk=lect_pk)

    context = {
        "form": ListenerForm(instance=listener),
        "title": "update listener",
        "listener": listener,
        "object": listener.lecture,
    }
    return render(request, "publicwork/listener_update.html", context)


@login_required
@permission_required("publicwork.delete_listener")
def remove_listener(request, lect_pk, lstn_pk):
    listener = Listener.objects.get(pk=lstn_pk)

    if request.method == "POST":
        listener.delete()
        return redirect("lecture_detail", pk=lect_pk)

    context = {"object": listener, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)


# from seeker side  ###########################################################
@login_required
@permission_required("publicwork.add_listener")
def add_frequency(request, pk):
    object_list = None
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
                request, "The seeker has been inserted on lecture!"
            )
            return redirect("seeker_frequencies", pk=pk)

        context = {
            "seeker": seeker,
            "form": ListenerForm,
            "insert_to": f"{lecture.theme} - {lecture.center}",
            "title": "confirm to insert",
        }
        return render(
            request,
            "publicwork/elements/confirm_add_listener.html",
            context,
        )

    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset, page = search_lecture(request, Lecture)
        object_list = paginator(queryset, page=page)
        # add action links
        for item in object_list:
            item.add_link = reverse("add_frequency", args=[pk])

    context = {
        "object": seeker,
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("seeker_home"),
        "title": "add frequency",
        "type_list": LECTURE_TYPES,
        "pre_freqs": [lect.pk for lect in seeker.lecture_set.all()],
        "tab": "frequencies",
        "add": True,
        "goback": reverse("seeker_frequencies", args=[pk]),
    }
    return render(request, "publicwork/seeker_add_or_change.html", context)


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
        messages.success(request, "The Listener has been updated!")
        return redirect("seeker_frequencies", pk=seek_pk)

    context = {
        "object": seeker,
        "listener": listener,
        "form": ListenerForm(instance=listener),
        "title": "update frequency | seeker side",
        "seeker_side": True,
        "goback": reverse("seeker_frequencies", args=[seek_pk]),
    }
    return render(request, "publicwork/listener_update.html", context)


@login_required
@permission_required("publicwork.delete_listener")
def remove_frequency(request, seek_pk, freq_pk):
    listener = Listener.objects.get(pk=freq_pk)

    if request.method == "POST":
        listener.delete()
        return redirect("seeker_frequencies", pk=seek_pk)

    context = {"object": listener, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)
