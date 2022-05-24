from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import (
    paginator,
    belongs_center,
    clear_session,
    SEEKER_STATUS,
)

from center.models import Center
from base.searchs import search_seeker

from ..forms import SeekerForm
from ..models import Seeker


@login_required
@permission_required("publicwork.view_seeker")
def seeker_home(request):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "publicwork/seeker/elements/seeker_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "publicwork/seeker/home.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    object_list = None
    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset = search_seeker(request, Seeker)
        object_list = queryset[_from:_to]
        # add action links
        for item in object_list:
            item.to_detail = reverse("seeker_detail", args=[item.pk])
            item.local = f"{item.city} ({item.state}-{item.country})"

    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("seeker_home"),
        "status_list": SEEKER_STATUS,
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
            return redirect(reverse("seeker_home") + "?init=on")

    context = {
        "form": SeekerForm(
            initial={
                "made_by": request.user,
                "center": request.user.person.center,
            }
        ),
        "form_name": "Seeker",
        "form_path": "publicwork/forms/seeker.html",
        "goback": reverse("seeker_home"),
        "title": _("create seeker"),
        "to_create": True,
    }
    return render(request, "base/form.html", context)


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

    context = {
        "form": seeker_form,
        "form_name": "Seeker",
        "form_path": "publicwork/forms/seeker.html",
        "goback": reverse("seeker_detail", args=[pk]),
        "title": _("update seeker"),
        "pk": pk,
    }
    return render(request, "base/form.html", context)


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

    context = {
        "object": seeker,
        "title": _("confirm to delete"),
    }
    return render(request, "base/confirm_delete.html", context)


@login_required
@permission_required("publicwork.add_seeker")
def seeker_reinsert(request, pk):
    seeker = Seeker.objects.get(pk=pk)
    if request.method == "POST":
        seeker.is_active = True
        seeker.save()
        return redirect(reverse("seeker_home") + "?init=on")

    context = {"object": seeker, "title": _("confirm to reinsert")}
    return render(
        request, "publicwork/seeker/confirm_to_reinsert.html", context
    )


# seeker frequencies
@login_required
@permission_required("publicwork.view_seeker")
def seeker_frequencies(request, pk):
    belongs_center(request, pk, Seeker)
    page = request.GET["page"] if request.GET.get("page") else 1

    seeker = Seeker.objects.get(pk=pk)
    frequencies = seeker.listener_set.all()
    ranking = sum([f.ranking for f in frequencies])

    context = {
        "object": seeker,
        "title": _("seeker detail | frequencies"),
        "object_list": paginator(frequencies, page=page),
        "nav": "seeker",
        "tab": "frequencies",
        "ranking": ranking,
    }

    return render(request, "publicwork/seeker/detail.html", context)


# seeker historic
@login_required
@permission_required("publicwork.view_seeker")
def seeker_historic(request, pk):
    belongs_center(request, pk, Seeker)
    page = request.GET["page"] if request.GET.get("page") else 1

    seeker = Seeker.objects.get(pk=pk)
    historics = seeker.historicofseeker_set.all().order_by("-date")

    object_list = paginator(historics, page=page)
    # add action links
    for item in object_list:
        item.click_link = reverse("update_historic", args=[pk, item.pk])

    context = {
        "object": seeker,
        "title": _("seeker detail | historic"),
        "object_list": object_list,
        "nav": "seeker",
        "tab": "historic",
    }

    return render(request, "publicwork/seeker/detail.html", context)
