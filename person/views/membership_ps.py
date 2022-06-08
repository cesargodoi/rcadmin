from django.http import QueryDict
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import (
    WORKGROUP_TYPES,
    paginator,
    clear_session,
    get_template_and_pagination,
)
from workgroup.forms import MembershipForm
from workgroup.models import Membership, Workgroup
from base.searchs import search_workgroup

from ..models import Person


@login_required
@permission_required("workgroup.view_membership")
def membership_ps_list(request, person_id):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request, "person/detail.html", "person/elements/membership_list.html"
    )

    queryset = Membership.objects.filter(person=person_id).order_by(
        "workgroup"
    )
    person = (
        queryset[0].person if queryset else Person.objects.get(id=person_id)
    )
    count = len(queryset)
    object_list = queryset[_from:_to]

    # add action links
    for item in object_list:
        item.update_link = reverse(
            "membership_ps_update", args=[person_id, item.pk]
        )
        item.del_link = reverse(
            "membership_ps_delete", args=[person_id, item.pk]
        )

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "title": _("membership list"),
        "object": person,  # to header element
        "nav": "detail",
        "tab": "membership",
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.add_membership")
def membership_ps_create(request, person_id):
    object_list = None
    person = Person.objects.get(id=person_id)

    if request.GET.get("pk"):
        workgroup = Workgroup.objects.get(pk=request.GET.get("pk"))

        if request.method == "POST":
            workgroup.members.add(person)
            messages.success(
                request, "The person has been inserted on workgroup!"
            )
            return redirect("membership_ps_list", person_id=person_id)

        context = {
            "insert_to": f"{workgroup.name} {workgroup.center}",
            "title": _("confirm to insert"),
            "person": person,  # to header element
        }
        return render(
            request, "person/elements/confirm_to_insert.html", context
        )

    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "person/membership_ps_insert.html",
        "person/elements/workgroup_list.html",
    )

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        queryset, count = search_workgroup(request, Workgroup, _from, _to)
        object_list = paginator(queryset, page=page)

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "title": _("insert membership"),
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("membership_ps_create", args=[person_id]),
        "workgroup_types": WORKGROUP_TYPES,
        "pre_groups": [
            person.workgroup.pk for person in person.membership_set.all()
        ],
        "person_id": person_id,  # to goback
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.change_membership")
def membership_ps_update(request, person_id, pk):
    membership = Membership.objects.get(pk=pk)

    if request.method == "POST":
        data = QueryDict(request.body).dict()
        form = MembershipForm(data, instance=membership)
        if form.is_valid():
            form.save()

            membership.update_link = reverse(
                "membership_ps_update", args=[person_id, pk]
            )
            membership.del_link = reverse(
                "membership_ps_delete", args=[person_id, pk]
            )

            template_name = "person/elements/hx/membership_updated.html"
            context = {"obj": membership, "pos": request.GET.get("pos")}
            return render(request, template_name, context)

    if request.method == "POSTi":
        form = MembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            messages.success(request, "The Membership has been updated!")

        return redirect("membership_ps_list", person_id=person_id)

    template_name = "person/forms/membership_update.html"
    context = {
        "form": MembershipForm(instance=membership),
        "object": membership,
        "to_update": reverse("membership_ps_update", args=[person_id, pk]),
        "mbr_pk": pk,
        "pos": request.GET.get("pos"),
    }
    return render(request, template_name, context)


@require_http_methods(["DELETE"])
@login_required
@permission_required("workgroup.delete_membership")
def membership_ps_delete(request, person_id, pk):
    Membership.objects.get(pk=pk).delete()
    return redirect("membership_ps_list", person_id=person_id)
