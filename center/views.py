from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.http import QueryDict
from django.urls import reverse
from django.utils.translation import gettext as _
from rcadmin.common import clear_session
from base.searchs import search_center
from django.http.response import Http404
from person.models import Person

from rcadmin.common import get_template_and_pagination
from .forms import (
    CenterForm,
    SelectNewCenterForm,
    BasicCenterForm,
    AddressCenterForm,
    OthersCenterForm,
    ImageCenterForm,
)
from .models import Center


@login_required
@permission_required("center.view_center")
def center_home(request):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request, "center/home.html", "center/elements/center_list.html"
    )

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_center(request, Center, _from, _to)
        # add action links
        for item in object_list:
            item.click_link = reverse("center_detail", args=[item.pk])

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
        "title": _("center home"),
        "nav": "home",
    }
    return render(request, template_name, context)


@login_required
@permission_required("center.view_center")
def center_detail(request, pk):
    center = Center.objects.get(pk=pk)
    users = center.person_set.filter(is_active=True).count()
    goback = (
        reverse("home") if request.GET.get("from") else reverse("center_home")
    )

    context = {
        "object": center,
        "title": _("center detail"),
        "users": users,
        "nav": "detail",
        "goback": goback,
    }
    return render(request, "center/detail.html", context)


@login_required
@permission_required("center.add_center")
def center_create(request):
    if request.method == "POST":
        data = QueryDict(request.body).dict()
        form = CenterForm(data, request.FILES)
        if form.is_valid():
            form.save()

            message = f"The Center '{data['name']}' has been created!"
            messages.success(request, message)

            center = Center.objects.get(name=data["name"])
            return redirect(reverse("center_detail", args=[center.id]))
        else:
            message = "There are some errors in the form, please correct them."
            messages.warning(request, message)

    template_name = "center/forms/create_center.html"
    context = {
        "form": CenterForm(
            request.POST or None, initial={"made_by": request.user}
        ),
        "callback_link": reverse("center_create"),
        "title": _("Create center"),
    }
    return render(request, template_name, context)


@login_required
@permission_required("center.change_center")
def center_update_basic(request, pk):
    persons = [psn.id for psn in Person.objects.filter(center=pk)]
    if request.user.person.pk in persons or request.user.is_superuser:
        center = Center.objects.get(pk=pk)

        if request.method == "POST":
            form = BasicCenterForm(request.POST, instance=center)
            if form.is_valid():
                form.save()
                message = (
                    f"The Center '{request.POST['name']}' has been updated!"
                )
                messages.success(request, message)
            return redirect("center_detail", pk=pk)
    else:
        raise Http404

    template_name = "center/forms/tab_basic.html"
    context = {
        "title": _("Update basic info"),
        "form": BasicCenterForm(instance=center),
        "callback_link": reverse("center_update_basic", args=[pk]),
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("center.change_center")
def center_update_address(request, pk):
    persons = [psn.id for psn in Person.objects.filter(center=pk)]
    if request.user.person.pk in persons or request.user.is_superuser:
        center = Center.objects.get(pk=pk)

        if request.method == "POST":
            form = AddressCenterForm(request.POST, instance=center)
            if form.is_valid():
                form.save()

            template_name = "center/elements/tab_address.html"
            return render(request, template_name, {"object": center})

    else:
        raise Http404

    template_name = "center/forms/tab_address.html"
    context = {
        "title": _("Update address info"),
        "form": AddressCenterForm(instance=center),
        "callback_link": reverse("center_update_address", args=[pk]),
        "target": "tabAddress",
        "swap": "innerHTML",
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("center.change_center")
def center_update_others(request, pk):
    persons = [psn.id for psn in Person.objects.filter(center=pk)]
    if request.user.person.pk in persons or request.user.is_superuser:
        center = Center.objects.get(pk=pk)

        if request.method == "POST":
            form = OthersCenterForm(
                request.POST, request.FILES, instance=center
            )
            if form.is_valid():
                form.save()

            template_name = "center/elements/tab_others.html"
            return render(request, template_name, {"object": center})

    else:
        raise Http404

    template_name = "center/forms/tab_others.html"
    context = {
        "title": _("Update others info"),
        "form": OthersCenterForm(instance=center),
        "callback_link": reverse("center_update_others", args=[pk]),
        "target": "tabOthers",
        "swap": "innerHTML",
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("center.change_center")
def center_update_image(request, pk):
    persons = [psn.id for psn in Person.objects.filter(center=pk)]
    if request.user.person.pk in persons or request.user.is_superuser:
        center = Center.objects.get(pk=pk)

        if request.method == "POST":
            form = ImageCenterForm(
                request.POST, request.FILES, instance=center
            )
            if form.is_valid():
                form.save()

            return redirect("center_detail", pk=pk)

    else:
        raise Http404

    template_name = "center/forms/tab_image.html"
    context = {
        "title": _("Update image info"),
        "form": ImageCenterForm(instance=center),
        "callback_link": reverse("center_update_image", args=[pk]),
        "target": "tabImage",
        "swap": "innerHTML",
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("center.delete_center")
def center_delete(request, pk):
    center = Center.objects.get(pk=pk)
    if request.method == "POST":
        # new_center returns conf_center
        if request.POST.get("conf_center"):
            _center = Center.objects.get(pk=request.POST.get("conf_center"))
            persons = center.person_set.all()
            for person in persons:
                person.center = _center
                person.save()
        center.is_active = False
        center.save()
        return redirect("center_home")

    template_name = "center/confirm/delete.html"
    context = {
        "object": center,
        "del_link": reverse("center_delete", args=[pk]),
        "new_center": SelectNewCenterForm() if center.person_set.all() else "",
    }
    return render(request, template_name, context)


@login_required
@permission_required("center.add_center")
def center_reinsert(request, pk):
    center = Center.objects.get(pk=pk)
    if request.method == "POST":
        center.is_active = True
        center.save()
        return redirect("center_home")

    template_name = "center/confirm/reinsert.html"
    context = {
        "object": center,
        "reinsert_link": reverse("center_reinsert", args=[pk]),
    }
    return render(request, template_name, context)
