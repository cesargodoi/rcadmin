from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import (
    belongs_center,
    clear_session,
    SEEKER_STATUS,
    get_template_and_pagination,
)

from center.models import Center
from base.searchs import search_seeker

from ..forms import SeekerForm
from ..models import Seeker


@login_required
@permission_required("publicwork.view_seeker")
def seeker_home(request):
    clear_session(request, ["pwg"])

    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/seeker/home.html",
        "publicwork/seeker/elements/seeker_list.html",
    )

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_seeker(request, Seeker, _from, _to)
        # add action links
        for item in object_list:
            item.to_detail = reverse("seeker_detail", args=[item.pk])
            item.local = f"{item.city} ({item.state}-{item.country})"

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
        "goback_link": reverse("seeker_home"),
        "status_list": [stt for stt in SEEKER_STATUS if stt[0] != "OBS"],
        "title": _("seeker home"),
        "centers": [[str(cnt.pk), str(cnt)] for cnt in Center.objects.all()],
        "user_center": str(request.user.person.center.pk),
        "nav": "sk_home",
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.view_seeker")
def seeker_detail(request, pk):
    belongs_center(request, pk, Seeker)
    seeker = Seeker.objects.get(pk=pk)
    age = (date.today() - seeker.birth).days // 365
    if request.GET.get("pwg"):
        request.session["pwg"] = request.GET["pwg"]
    context = {
        "object": seeker,
        "title": _("seeker detail"),
        "nav": "seeker",
        "tab": "info",
        "age": age,
    }
    return render(request, "publicwork/seeker/detail.html", context)


@login_required
@permission_required("publicwork.add_seeker")
def seeker_create(request):
    if request.method == "POST":
        seeker_form = SeekerForm(request.POST, request.FILES)
        if seeker_form.is_valid():
            seeker_form.save()

            message = f"The Seeker '{request.POST['name']}' has been created!"
            messages.success(request, message)

        return redirect("seeker_home")

    seeker_form = SeekerForm(
        initial={
            "made_by": request.user,
            "center": request.user.person.center,
        }
    )

    template_name = "publicwork/seeker/forms/seeker.html"
    context = {
        "form": seeker_form,
        "callback": reverse("seeker_create"),
        "title": _("Create seeker"),
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.change_seeker")
def seeker_update(request, pk):
    belongs_center(request, pk, Seeker)

    seeker = Seeker.objects.get(pk=pk)
    if request.method == "POST":
        seeker_form = SeekerForm(request.POST, request.FILES, instance=seeker)
        if seeker_form.is_valid():
            seeker_form.save()
            message = f"The Seeker '{request.POST['name']}' has been updated!"
            messages.success(request, message)

        return redirect("seeker_detail", pk=pk)

    seeker_form = SeekerForm(
        instance=seeker,
        initial={"made_by": request.user},
    )

    template_name = "publicwork/seeker/forms/seeker.html"
    context = {
        "form": seeker_form,
        "callback": reverse("seeker_update", args=[pk]),
        "title": _("Update seeker"),
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.delete_seeker")
def seeker_delete(request, pk):
    seeker = Seeker.objects.get(pk=pk)

    if request.method == "POST":
        if seeker.listener_set.count():
            seeker.is_active = False
            seeker.save()
        else:
            if seeker.historicofseeker_set.count():
                seeker.historicofseeker_set.all().delete()
            seeker.delete()
        return redirect("seeker_home")

    template_name = "publicwork/confirm/delete.html"
    context = {
        "object": seeker,
        "del_link": reverse("seeker_delete", args=[pk]),
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.add_seeker")
def seeker_reinsert(request, pk):
    seeker = Seeker.objects.get(pk=pk)

    if request.method == "POST":
        seeker.is_active = True
        seeker.save()
        return redirect("seeker_home")

    template_name = "publicwork/confirm/reinsert.html"
    context = {
        "object": seeker,
        "reinsert_link": reverse("seeker_reinsert", args=[pk]),
    }
    return render(request, template_name, context)


# seeker frequencies
@login_required
@permission_required("publicwork.view_seeker")
def seeker_frequencies(request, pk):
    belongs_center(request, pk, Seeker)

    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/seeker/detail.html",
        "publicwork/seeker/elements/frequency_list.html",
    )

    seeker = Seeker.objects.get(pk=pk)
    _object_list = seeker.listener_set.all()

    count = len(_object_list)
    ranking = sum([f.ranking for f in _object_list])

    object_list = _object_list[_from:_to]
    # add action links
    for item in object_list:
        item.update_link = reverse("update_frequency", args=[pk, item.pk])
        item.delete_link = reverse("remove_frequency", args=[pk, item.pk])

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": seeker,
        "title": _("seeker detail | frequencies"),
        "nav": "seeker",
        "tab": "frequencies",
        "ranking": ranking,
    }

    return render(request, template_name, context)


# seeker historic
@login_required
@permission_required("publicwork.view_seeker")
def seeker_historic(request, pk):
    belongs_center(request, pk, Seeker)

    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/seeker/detail.html",
        "publicwork/seeker/elements/historic_list.html",
    )

    seeker = Seeker.objects.get(pk=pk)
    _object_list = seeker.historicofseeker_set.all().order_by("-date")

    count = len(_object_list)
    object_list = _object_list[_from:_to]
    # add action links
    for item in object_list:
        item.update_link = reverse("update_historic", args=[pk, item.pk])
        item.delete_link = reverse("delete_historic", args=[pk, item.pk])

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": seeker,
        "title": _("seeker detail | historic"),
        "nav": "seeker",
        "tab": "historic",
    }

    return render(request, template_name, context)
