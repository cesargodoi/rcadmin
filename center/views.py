import json

from django.template.loader import render_to_string
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import clear_session
from base.searchs import search_center, search_person
from django.http.response import Http404
from user.models import User
from person.models import Person

from rcadmin.common import get_pagination, get_template_and_pagination
from .forms import (
    CenterForm,
    SelectNewCenterForm,
    InfoCenterForm,
    OthersCenterForm,
    ImageCenterForm,
    ResponsibleForm,
)
from .models import Center, Responsible


modal_updated_triggers = json.dumps(
    {
        "closeModal": True,
        "showToast": _("The Center has been updated!"),
    }
)


@login_required
@permission_required("center.view_center")
def center_home(request):
    clear_session(request, ["search"])
    context = {"title": _("centers"), "nav": "home"}
    return render(request, "center/home.html", context)


def center_list(request):
    page, _from, _to, LIMIT = get_pagination(request)

    if request.GET.get("clear") or not request.GET.get("term"):
        clear_session(request, ["search"])

    object_list, count = search_center(request, Center, _from, _to)
    for item in object_list:
        item.click_link = reverse("center_detail", args=[item.pk])

    template_name = "center/elements/center_list.html"
    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "clear_search": True if request.GET.get("clear") else False,
    }
    return HttpResponse(render_to_string(template_name, context, request))


@login_required
@permission_required("center.view_center")
def center_detail(request, pk):
    clear_session(request, ["search"])
    center = Center.objects.get(pk=pk)
    center.active_users = center.person_set.filter(is_active=True).count()

    template_name = "center/detail.html"
    context = {
        "title": _("center detail"),
        "object": center,
        "nav": "detail",
        "goback": (
            reverse("home")
            if request.GET.get("from")
            else reverse("center_home")
        ),
    }
    return render(request, template_name, context)


@login_required
@permission_required("center.add_center")
def center_create(request):
    template_name = "center/forms/create_center.html"
    if request.method == "POST":
        form = CenterForm(request.POST, request.FILES)
        if form.is_valid():
            center = form.save()
            return HttpResponse(
                headers={
                    "HX-redirect": reverse("center_detail", args=[center.pk]),
                },
            )
    else:
        # select only conference centers to field "conf_center"
        CenterForm.base_fields["conf_center"] = forms.ModelChoiceField(
            required=False, queryset=Center.objects.filter(center_type="CNF")
        )
        form = CenterForm(
            request.POST or None, initial={"made_by": request.user}
        )

    context = {"title": _("Create center"), "form": form}
    return render(request, template_name, context)


@login_required
@permission_required("center.change_center")
def center_update_info(request, pk):
    template_name = "center/forms/update_info.html"
    center = Center.objects.get(pk=pk)
    center_users = User.objects.filter(person__center=center)

    if request.user not in center_users and not request.user.is_superuser:
        raise Http404

    if request.method == "POST":
        form = InfoCenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            template_name = "center/elements/tab_info.html"
            context = {"object": center, "updated": True}
            return HttpResponse(
                render_to_string(template_name, context, request),
                headers={
                    "HX-Retarget": "#tabInfo",
                    "HX-Trigger": modal_updated_triggers,
                },
            )
    else:
        # select only conference centers to field "conf_center"
        InfoCenterForm.base_fields["conf_center"] = forms.ModelChoiceField(
            required=False, queryset=Center.objects.filter(center_type="CNF")
        )
        form = InfoCenterForm(
            instance=center, initial={"made_by": request.user}
        )

    context = {"title": _("Update info"), "form": form}
    return render(request, template_name, context)


@login_required
@permission_required("center.change_center")
def center_update_image(request, pk):
    template_name = "center/forms/update_image.html"
    center = Center.objects.get(pk=pk)
    center_users = User.objects.filter(person__center=center)

    if request.user not in center_users and not request.user.is_superuser:
        raise Http404

    if request.method == "POST":
        form = ImageCenterForm(request.POST, request.FILES, instance=center)
        if form.is_valid():
            form.save()
            template_name = "center/elements/tab_image.html"
            context = {"object": center}
            return HttpResponse(
                render_to_string(template_name, context, request),
                headers={
                    "HX-Retarget": "#tabImage",
                    "HX-Trigger": modal_updated_triggers,
                },
            )
    else:
        form = ImageCenterForm(instance=center)

    context = {"title": _("Update image"), "form": form}
    return render(request, template_name, context)


@login_required
@permission_required("center.change_center")
def center_update_others(request, pk):
    template_name = "center/forms/update_others.html"
    center = Center.objects.get(pk=pk)
    center_users = User.objects.filter(person__center=center)

    if request.user not in center_users and not request.user.is_superuser:
        raise Http404

    if request.method == "POST":
        form = OthersCenterForm(request.POST, request.FILES, instance=center)
        if form.is_valid():
            form.save()
            template_name = "center/elements/tab_others.html"
            context = {"object": center, "updated": True}
            return HttpResponse(
                render_to_string(template_name, context, request),
                headers={
                    "HX-Retarget": "#tabOthers",
                    "HX-Trigger": modal_updated_triggers,
                },
            )
    else:
        form = OthersCenterForm(
            instance=center, initial={"made_by": request.user}
        )

    context = {"title": _("Update others info"), "form": form}
    return render(request, template_name, context)


@login_required
@permission_required("center.delete_center")
def center_delete(request, pk):
    center = Center.objects.get(pk=pk)
    if request.method == "POST":
        if request.POST.get("conf_center"):
            _center = Center.objects.get(pk=request.POST.get("conf_center"))
            persons = center.person_set.all()
            for person in persons:
                person.center = _center
                person.save()

        if center_sets(center):
            center.is_active = False
            center.save()
        else:
            center.delete()

        return redirect("center_home")

    template_name = "center/confirm/delete.html"
    context = {
        "object": center,
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


#  manage responsibles  #######################################################
@login_required
@permission_required("center.add_center")
def center_add_responsible(request, pk):
    center = Center.objects.get(pk=pk)
    center_users = User.objects.filter(person__center=center)
    if request.user not in center_users and not request.user.is_superuser:
        raise Http404

    if request.GET.get("psn_pk"):
        person = Person.objects.get(pk=request.GET["psn_pk"])

        if request.method == "POST":
            form = ResponsibleForm(request.POST)
            if form.is_valid():
                form.save()
                # TODO - Fazer validação para inserir (o não) de permissão.
                return HttpResponse(
                    headers={
                        "HX-Redirect": reverse(
                            "center_detail", args=[center.pk]
                        ),
                    },
                )

        form = ResponsibleForm(initial={"center": center, "user": person.user})
        template_name = "center/forms/add_responsible.html"
        context = {
            "object": f"{center} ➜ {person}",
            "form": form,
            "confirm_link": f"{request.path}?psn_pk={request.GET['psn_pk']}",
        }
        return render(request, template_name, context)

    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "center/add_responsible.html",
        "center/elements/person_list.html",
    )

    object_list, count = search_person(request, Person, _from, _to)
    for item in object_list:
        item.add_resp = f"{request.path}?psn_pk={item.pk}"

    if not request.htmx and object_list:
        message = f"{count} records were found in the database"
        messages.success(request, message)

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "title": _("add responsible"),
        "pk": pk,
    }
    return render(request, template_name, context)


@login_required
@permission_required("center.add_center")
def center_del_responsible(request, pk):
    responsible = Responsible.objects.get(pk=pk)
    _user = responsible.user.person.name
    if request.method == "POST":
        responsible.delete()
        # TODO - Fazer validação para retirada (o não) de permissão.
        template_name = "center/elements/tab_responsibles.html"
        context = {"object": Center.objects.get(pk=responsible.center.pk)}
        return HttpResponse(
            render_to_string(template_name, context, request),
            headers={
                "HX-Retarget": "#tabResponsibles",
                "HX-Trigger": json.dumps(
                    {
                        "closeModal": True,
                        "showToast": _(f"The '{_user}' has been deleted!"),
                    }
                ),
            },
        )

    template_name = "center/confirm/delete_hx.html"
    context = {
        "object": "{} ⛔️ {}".format(
            responsible.user.person.name, responsible.center.name
        ),
    }
    return render(request, template_name, context)


#  handlers
def center_sets(center):
    if (
        center.center_set.all()
        or center.responsible_set.all()
        or center.lecture_set.all()
        or center.seeker_set.all()
        or center.person_set.all()
        or center.event_set.all()
        or center.order_set.all()
        or center.workgroup_set.all()
        or center.publicworkgroup_set.all()
    ):
        return True
