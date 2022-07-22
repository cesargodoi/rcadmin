from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

# from django.http import QueryDict
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import (
    WORKGROUP_TYPES,
    clear_session,
    get_template_and_pagination,
)
from base.searchs import search_workgroup

from ..forms import WorkgroupForm
from ..models import Workgroup


@login_required
@permission_required("workgroup.view_workgroup")
def workgroup_home(request):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "workgroup/home.html",
        "workgroup/elements/workgroup_list.html",
    )

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_workgroup(request, Workgroup, _from, _to)
        # add action links
        for item in object_list:
            item.click_link = reverse("workgroup_detail", args=[item.pk])

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
        "goback_link": reverse("workgroup_home"),
        "title": _("workgroups"),
        "workgroup_types": WORKGROUP_TYPES,
        "nav": "home",
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.view_workgroup")
def workgroup_detail(request, pk):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "workgroup/detail.html",
        "workgroup/member/elements/member_list.html",
    )

    object = Workgroup.objects.get(pk=pk)

    count = object.membership_set.all().count()
    object_list = object.membership_set.all().order_by("person__name_sa")[
        _from:_to
    ]

    # add action links
    for member in object_list:
        member.update_link = reverse("membership_update", args=[pk, member.pk])
        member.del_link = reverse("membership_delete", args=[pk, member.pk])

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object": object,
        "count": count,
        "object_list": object_list,
        "title": _("workgroup detail"),
        "nav": "detail",
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.add_workgroup")
def workgroup_create(request):
    if request.method == "POST":
        form = WorkgroupForm(request.POST)

        if form.is_valid():
            form.save()

        LIMIT, template_name, _from, _to, page = get_template_and_pagination(
            request,
            "workgroup/home.html",
            "workgroup/elements/workgroup_list.html",
        )

        object_list, count = search_workgroup(request, Workgroup, _from, _to)
        # add action links
        for item in object_list:
            item.click_link = reverse("workgroup_detail", args=[item.pk])

        template_name = "workgroup/elements/workgroup_list.html"
        context = {
            "LIMIT": LIMIT,
            "page": page,
            "counter": (page - 1) * LIMIT,
            "object_list": object_list,
            "count": count,
            "init": True if request.GET.get("init") else False,
            "nav": "home",
        }
        return render(request, template_name, context)

    template_name = "workgroup/forms/workgroup.html"
    context = {
        "title": _("Create workgroup"),
        "form": WorkgroupForm(
            initial={
                "made_by": request.user,
                "center": request.user.person.center,
                "workgroup_type": "MNT",
            }
        ),
        "callback_link": reverse("workgroup_create"),
        "target": "workgroupList",
        "swap": "innerHTML",
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.change_workgroup")
def workgroup_update(request, pk):
    workgroup = Workgroup.objects.get(pk=pk)

    if request.method == "POST":
        form = WorkgroupForm(request.POST, instance=workgroup)
        if form.is_valid():
            form.save()

        template_name = "workgroup/header.html"
        context = {"object": Workgroup.objects.get(pk=pk)}
        return render(request, template_name, context)

    template_name = "workgroup/forms/workgroup.html"
    context = {
        "title": _("Update workgroup"),
        "form": WorkgroupForm(
            instance=workgroup, initial={"made_by": request.user}
        ),
        "callback_link": reverse("workgroup_update", args=[pk]),
        "target": "workgroupHeader",
        "swap": "innerHTML",
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.delete_workgroup")
def workgroup_delete(request, pk):
    workgroup = Workgroup.objects.get(pk=pk)

    if request.method == "POST":
        if workgroup.members:
            workgroup.members.clear()
        workgroup.delete()
        return redirect("workgroup_home")

    template_name = "workgroup/confirm/delete.html"
    context = {
        "object": workgroup,
        "del_link": reverse("workgroup_delete", args=[pk]),
    }
    return render(request, template_name, context)
