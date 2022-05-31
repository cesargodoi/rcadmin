from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group

from person.models import Person
from rcadmin.common import ASPECTS, STATUS, clear_session

from ..forms import MembershipForm
from ..models import Membership, Workgroup
from base.searchs import search_person


@login_required
@permission_required("workgroup.add_membership")
def membership_insert(request, workgroup_id):
    # set limit of registers
    LIMIT = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "workgroup/elements/person_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "workgroup/membership_insert.html"
        page = 1
    # get limitby
    _from, _to = LIMIT * (page - 1), LIMIT * page

    object_list = None
    workgroup = Workgroup.objects.get(pk=workgroup_id)

    if request.GET.get("pk"):
        person = Person.objects.get(pk=request.GET.get("pk"))

        if request.method == "POST":
            workgroup.members.add(person)
            messages.success(
                request, _("The person has been inserted on workgroup!")
            )
            return redirect("workgroup_detail", pk=workgroup_id)

        context = {
            "person": person,
            "insert_to": f"{workgroup.name} {workgroup.center}",
            "title": _("confirm to insert"),
        }
        return render(
            request,
            "workgroup/elements/confirm_to_insert_membership.html",
            context,
        )
    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset = search_person(request, Person)
        object_list = queryset[_from:_to]
        # add action links
        for item in object_list:
            item.add_link = (
                reverse("membership_insert", args=[workgroup_id])
                + f"?pk={ item.pk }"
            )
            item.local = "{} ({}-{})".format(
                item.user.profile.city,
                item.user.profile.state,
                item.user.profile.country,
            )

    context = {
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "aspect_list": ASPECTS,
        "status_list": STATUS,
        "title": _("create membership"),
        "goback_link": reverse("membership_insert", args=[workgroup.pk]),
        "form": MembershipForm(initial={"workgroup": workgroup}),
        "object": workgroup,
        "flag": "membership",
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.change_membership")
def membership_update(request, workgroup_id, pk):
    membership = Membership.objects.get(pk=pk)

    if request.method == "POST":
        form = MembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            ensure_mentoring_permission(form.cleaned_data["person"])

            messages.success(request, _("The Membership has been updated!"))

        return redirect("workgroup_detail", pk=workgroup_id)

    context = {
        "form": MembershipForm(instance=membership),
        "title": _("update membership"),
        "object": membership.workgroup,
    }
    return render(request, "workgroup/membership_update.html", context)


@login_required
@permission_required("workgroup.delete_membership")
def membership_delete(request, workgroup_id, pk):
    membership = Membership.objects.get(pk=pk)
    if request.method == "POST":
        membership.delete()
        return redirect("workgroup_detail", pk=workgroup_id)

    context = {
        "object": membership,
        "title": _("confirm to delete"),
    }
    return render(request, "base/confirm_delete.html", context)


#  handlers
def ensure_mentoring_permission(person):
    mentor = [g for g in person.membership_set.all() if g.role_type == "MTR"]
    mentoring = Group.objects.get(name="mentoring")
    if mentor:
        person.user.groups.add(mentoring)
    else:
        person.user.groups.remove(mentoring)
