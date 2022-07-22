from django.http import QueryDict
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group

from person.models import Person
from rcadmin.common import (
    ASPECTS,
    STATUS,
    clear_session,
    get_template_and_pagination,
)

from ..forms import MembershipForm
from ..models import Membership, Workgroup
from base.searchs import search_person


@login_required
@permission_required("workgroup.add_membership")
def membership_insert(request, workgroup_id):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "workgroup/membership_insert.html",
        "workgroup/elements/person_list.html",
    )

    workgroup = Workgroup.objects.get(pk=workgroup_id)

    if request.GET.get("pk"):
        person = Person.objects.get(pk=request.GET.get("pk"))

        if request.method == "POST":
            workgroup.members.add(person)
            messages.success(
                request, _("The person has been inserted on workgroup!")
            )
            return redirect("workgroup_detail", pk=workgroup_id)
        template_name = ("workgroup/confirm/insert.html",)
        context = {
            "object": "{} ➜ {}".format(person.name, workgroup.name),
            "confirm_link": reverse(membership_insert, args=[workgroup_id])
            + f"?pk={request.GET.get('pk')}",
        }
        return render(request, template_name, context)

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_person(request, Person, _from, _to)
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
        data = QueryDict(request.body).dict()
        form = MembershipForm(data, instance=membership)
        if form.is_valid():
            form.save()
            ensure_mentoring_permission(form.cleaned_data["person"])

            membership.update_link = reverse(
                "membership_update", args=[workgroup_id, pk]
            )
            membership.del_link = reverse(
                "membership_delete", args=[workgroup_id, pk]
            )

            template_name = "workgroup/member/elements/hx/member_updated.html"
            context = {"obj": membership, "pos": request.GET.get("pos")}
            return render(request, template_name, context)

    template_name = "workgroup/forms/membership_update.html"
    context = {
        "form": MembershipForm(instance=membership),
        "object": membership,
        "to_update": reverse("membership_update", args=[workgroup_id, pk]),
        "mbr_pk": pk,
        "pos": request.GET.get("pos"),
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.delete_membership")
def membership_delete(request, workgroup_id, pk):
    membership = Membership.objects.get(pk=pk)

    if request.method == "POST":
        membership.delete()
        return redirect("workgroup_detail", pk=workgroup_id)

    template_name = "workgroup/confirm/delete.html"
    context = {
        "object": "{} ⛔️ {}".format(
            membership.person.name, membership.workgroup.name
        ),
        # "object": membership,
        "del_link": reverse("membership_delete", args=[workgroup_id, pk]),
    }
    return render(request, template_name, context)


#  handlers
def ensure_mentoring_permission(person):
    mentor = [g for g in person.membership_set.all() if g.role_type == "MTR"]
    mentoring = Group.objects.get(name="mentoring")
    if mentor:
        person.user.groups.add(mentoring)
    else:
        person.user.groups.remove(mentoring)
