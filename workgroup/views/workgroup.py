from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import WORKGROUP_TYPES, clear_session
from base.searchs import search_workgroup

from ..forms import WorkgroupForm
from ..models import Workgroup


@login_required
@permission_required("workgroup.view_workgroup")
def workgroup_home(request):
    # set limit of registers
    LIMIT = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "workgroup/elements/workgroup_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "workgroup/home.html"
        page = 1
    # get limitby
    _from, _to = LIMIT * (page - 1), LIMIT * page

    object_list = None
    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset = search_workgroup(request, Workgroup)
        object_list = queryset[_from:_to]
        # add action links
        for item in object_list:
            item.click_link = reverse("workgroup_detail", args=[item.pk])

    context = {
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
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
    # set limit of registers
    LIMIT = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "workgroup/member/elements/member_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "workgroup/detail.html"
        page = 1
    # get limitby
    _from, _to = LIMIT * (page - 1), LIMIT * page

    object = Workgroup.objects.get(pk=pk)

    queryset = object.membership_set.all().order_by("person__name_sa")

    object_list = queryset[_from:_to]

    # add action links
    for member in object_list:
        member.click_link = reverse("membership_update", args=[pk, member.pk])
        member.del_link = reverse("membership_delete", args=[pk, member.pk])

    context = {
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object": object,
        "object_list": object_list,
        "title": _("workgroup detail"),
        "nav": "detail",
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.add_workgroup")
def workgroup_create(request):
    template_name = "base/form.html"
    if request.method == "POST":
        form = WorkgroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("The Workgroup has been created!"))
        return redirect(reverse("workgroup_home") + "?init=on")

    context = {
        "form": WorkgroupForm(initial={"made_by": request.user}),
        "form_name": "Workgroup",
        "form_path": "workgroup/forms/workgroup.html",
        "goback": reverse("workgroup_home"),
        "title": _("create workgroup"),
        "to_create": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.change_workgroup")
def workgroup_update(request, pk):
    template_name = "base/form.html"
    workgroup = Workgroup.objects.get(pk=pk)
    if request.method == "POST":
        form = WorkgroupForm(request.POST, instance=workgroup)
        if form.is_valid():
            form.save()
            messages.success(request, _("The Workgroup has been updated!"))

        return redirect("workgroup_detail", pk=pk)

    context = {
        "form": WorkgroupForm(
            instance=workgroup, initial={"made_by": request.user}
        ),
        "form_name": "Workgroup",
        "form_path": "workgroup/forms/workgroup.html",
        "goback": reverse("workgroup_detail", args=[pk]),
        "title": _("update workgroup"),
        "pk": pk,
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.delete_workgroup")
def workgroup_delete(request, pk):
    template_name = "workgroup/elements/confirm_to_delete_workgroup.html"
    workgroup = Workgroup.objects.get(pk=pk)
    if request.method == "POST":
        if workgroup.members:
            workgroup.members.clear()
        workgroup.delete()
        return redirect("workgroup_home")

    context = {
        "object": workgroup,
        "members": [
            m
            for m in workgroup.membership_set.all().order_by("-role_type")[:4]
        ],
        "title": _("confirm to delete"),
    }
    return render(request, template_name, context)
