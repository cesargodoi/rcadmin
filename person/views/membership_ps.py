from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse

from schooladmin.common import WORKGROUP_TYPES, paginator, clear_session
from workgroup.forms import MembershipForm
from workgroup.models import Membership, Workgroup
from base.searchs import search_workgroup

from ..models import Person


@login_required
@permission_required("workgroup.view_membership")
def membership_ps_list(request, person_id):
    queryset = Membership.objects.filter(person=person_id).order_by(
        "workgroup"
    )
    person = (
        queryset[0].person if queryset else Person.objects.get(id=person_id)
    )
    object_list = paginator(queryset, page=request.GET.get("page"))

    context = {
        "object_list": object_list,
        "title": "membership list",
        "person": person,  # to header element
        "nav": "detail",
        "tab": "membership",
    }
    return render(request, "person/person_detail.html", context)


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
            "title": "confirm to insert",
            "person": person,  # to header element
        }
        return render(
            request, "person/elements/confirm_to_insert.html", context
        )

    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset, page = search_workgroup(request, Workgroup)
        object_list = paginator(queryset, page=page)

    context = {
        "object_list": object_list,
        "title": "insert membership",
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("membership_ps_create", args=[person_id]),
        "person": person,  # to header element
        "workgroup_types": WORKGROUP_TYPES,
        "pre_groups": [
            person.workgroup.pk for person in person.membership_set.all()
        ],
    }
    return render(request, "person/membership_ps_insert.html", context)


@login_required
@permission_required("workgroup.change_membership")
def membership_ps_update(request, person_id, pk):
    membership = Membership.objects.get(pk=pk)

    if request.method == "POST":
        form = MembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            messages.success(request, "The Membership has been updated!")

        return redirect("membership_ps_list", person_id=person_id)

    context = {
        "form": MembershipForm(instance=membership),
        "title": "update membership",
        "person": membership.person,  # to header element
    }
    return render(request, "person/forms/membership.html", context)


@login_required
@permission_required("workgroup.delete_membership")
def membership_ps_delete(request, person_id, pk):
    membership = Membership.objects.get(pk=pk)
    if request.method == "POST":
        membership.delete()
        return redirect("membership_ps_list", person_id=person_id)

    context = {"object": membership, "title": "confirm to delete"}
    return render(
        request, "person/elements/confirm_to_delete_member.html", context
    )
