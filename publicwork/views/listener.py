from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from rcadmin.common import (
    clear_session,
    SEEKER_STATUS,
    LECTURE_TYPES,
    get_template_and_pagination,
)
from django.urls import reverse

from center.models import Center
from base.searchs import search_seeker, search_lecture

from ..forms import ListenerForm
from ..models import Lecture, Seeker, Listener


@login_required
@permission_required("publicwork.add_listener")
def add_listener(request, lect_pk):
    lecture = Lecture.objects.get(pk=lect_pk)

    if request.GET.get("seek_pk"):
        seeker = Seeker.objects.get(pk=request.GET["seek_pk"])

        if request.method == "POST":
            # create listener
            Listener.objects.create(
                lecture=lecture,
                seeker=seeker,
                observations=request.POST["observations"],
            )
            messages.success(
                request, _("The seeker has been inserted on lecture!")
            )
            return redirect("lecture_detail", pk=lect_pk)

        template_name = "publicwork/listener/confirm/insert.html"
        context = {
            "seeker": seeker,
            "lecture": lecture,
            "form": ListenerForm,
            "title": _("Confirm to insert"),
            "callback": reverse("add_listener", args=[lect_pk])
            + f"?seek_pk={request.GET['seek_pk']}",
        }
        return render(request, template_name, context)

    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/listener/add.html",
        "publicwork/listener/elements/seeker_list.html",
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
        "status_list": [
            stt
            for stt in SEEKER_STATUS
            if stt[0] not in ("OBS", "ITD", "STD", "RST")
        ],
        "only_actives": True,
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
        listener.observations = request.POST["observations"]
        listener.save()
        messages.success(request, _("The Listener has been updated!"))

        return redirect("lecture_detail", pk=lect_pk)

    template_name = "publicwork/listener/forms/listener.html"
    context = {
        "form": ListenerForm(instance=listener),
        "object": listener,
        "callback": reverse("update_listener", args=[lect_pk, lstn_pk]),
        "title": _("Update listener"),
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.delete_listener")
def remove_listener(request, lect_pk, lstn_pk):
    listener = Listener.objects.get(pk=lstn_pk)

    if request.method == "POST":
        listener.delete()
        return redirect("lecture_detail", pk=lect_pk)

    template_name = "publicwork/confirm/delete.html"
    context = {
        "object": "{} ⛔️ {} ({})".format(
            listener.seeker.name,
            listener.lecture.theme,
            listener.lecture.center,
        ),
        "del_link": reverse("remove_listener", args=[lect_pk, lstn_pk]),
    }
    return render(request, template_name, context)


# from seeker side  ###########################################################
@login_required
@permission_required("publicwork.add_listener")
def add_frequency(request, pk):
    seeker = Seeker.objects.get(pk=pk)

    if request.GET.get("lect_pk"):
        lecture = Lecture.objects.get(pk=request.GET["lect_pk"])

        if request.method == "POST":
            # create listener
            Listener.objects.create(
                lecture=lecture,
                seeker=seeker,
                observations=request.POST["observations"],
            )
            messages.success(
                request, _("The seeker has been inserted on lecture!")
            )
            return redirect("seeker_frequencies", pk=pk)

        template_name = "publicwork/listener/confirm/insert.html"
        context = {
            "seeker": seeker,
            "lecture": lecture,
            "form": ListenerForm,
            "title": _("Confirm to insert"),
            "callback": reverse("add_frequency", args=[pk])
            + f"?lect_pk={request.GET['lect_pk']}",
        }
        return render(request, template_name, context)

    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/seeker/add_or_change.html",
        "publicwork/listener/elements/lecture_list.html",
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
    listener = Listener.objects.get(pk=freq_pk)
    if request.method == "POST":
        listener.observations = request.POST["observations"]
        listener.save()

        listener.update_link = reverse(
            "update_frequency", args=[seek_pk, freq_pk]
        )
        listener.delete_link = reverse(
            "remove_frequency", args=[seek_pk, freq_pk]
        )

        template_name = "publicwork/seeker/elements/hx/frequency_updated.html"
        context = {"obj": listener, "pos": request.GET.get("pos")}
        return render(request, template_name, context)

    template_name = "publicwork/seeker/forms/frequency.html"
    context = {
        "object": listener,
        "form": ListenerForm(instance=listener),
        "title": _("Update frequency"),
        "callback_link": reverse("update_frequency", args=[seek_pk, freq_pk]),
        "target": f"FRQ{freq_pk}",
        "swap": "innerHTML",
        "pos": request.GET.get("pos"),
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.delete_listener")
def remove_frequency(request, seek_pk, freq_pk):
    listener = Listener.objects.get(pk=freq_pk)

    if request.method == "POST":
        listener.delete()
        return redirect("seeker_frequencies", pk=seek_pk)

    template_name = "publicwork/seeker/confirm/delete.html"
    context = {
        "object": "{} ⛔️ {} ({})".format(
            listener.seeker.name,
            listener.lecture.theme,
            listener.lecture.center,
        ),
        "callback": reverse("remove_frequency", args=[seek_pk, freq_pk]),
    }
    return render(request, template_name, context)
