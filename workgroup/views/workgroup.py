from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import WORKGROUP_TYPES, paginator, clear_session
from base.searchs import search_workgroup

from ..forms import WorkgroupForm
from ..models import Workgroup


@login_required
@permission_required("workgroup.view_workgroup")
def workgroup_home(request):
    object_list = None
    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset, page = search_workgroup(request, Workgroup)
        object_list = paginator(queryset, page=page)
        # add action links
        for item in object_list:
            item.click_link = reverse("workgroup_detail", args=[item.pk])

    context = {
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("workgroup_home"),
        "title": _("workgroups"),
        "workgroup_types": WORKGROUP_TYPES,
        "nav": "home",
    }
    return render(request, "workgroup/home.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def workgroup_detail(request, pk):
    obj = Workgroup.objects.get(pk=pk)

    queryset = obj.membership_set.all().order_by("person__name_sa")

    object_list = paginator(queryset, 25, request.GET.get("page"))
    # add action links
    for member in object_list:
        member.click_link = reverse("membership_update", args=[pk, member.pk])
        member.del_link = reverse("membership_delete", args=[pk, member.pk])

    context = {
        "object": obj,
        "object_list": object_list,
        "title": _("workgroup detail"),
        "nav": "detail",
    }
    return render(request, "workgroup/detail.html", context)


@login_required
@permission_required("workgroup.add_workgroup")
def workgroup_create(request):
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
    return render(request, "base/form.html", context)


@login_required
@permission_required("workgroup.change_workgroup")
def workgroup_update(request, pk):
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
    return render(request, "base/form.html", context)


@login_required
@permission_required("workgroup.delete_workgroup")
def workgroup_delete(request, pk):
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
    return render(
        request, "workgroup/elements/confirm_to_delete_workgroup.html", context
    )
