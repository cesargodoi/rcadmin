from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from rcadmin.common import (
    paginator,
    belongs_center,
    clear_session,
    SEEKER_STATUS,
    LECTURE_TYPES,
    ASPECTS,
    STATUS,
)

from center.models import Center
from person.models import Person
from base.searchs import (
    search_pw_group,
    search_lecture,
    search_seeker,
    search_person,
)

from ..forms import GroupForm
from ..models import (
    Seeker,
    Lecture,
    Listener,
    PublicworkGroup,
    HistoricOfSeeker,
)


@login_required
@permission_required("publicwork.view_publicworkgroup")
def group_home(request):
    object_list = None
    clear_session(request, ["pwg", "search", "frequencies"])

    if request.GET.get("init") or request.user.groups.filter(
        name="publicwork_jr"
    ):
        clear_session(request, ["search"])
        object_list = request.user.person.publicworkgroup_set.all()
        for item in object_list:
            item.actives = item.members.filter(is_active=True).count()
            item.click_link = reverse("group_detail", args=[item.pk])
    else:
        queryset, page = search_pw_group(request, PublicworkGroup)
        object_list = paginator(queryset, page=page)
        # add action links
        for item in object_list:
            item.actives = item.members.filter(is_active=True).count()
            item.click_link = reverse("group_detail", args=[item.pk])

    context = {
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("group_home"),
        "title": _("public work - groups"),
        "centers": [[str(cnt.pk), str(cnt)] for cnt in Center.objects.all()],
        "user_center": str(request.user.person.center.pk),
        "nav": "gp_home",
    }
    return render(request, "publicwork/groups/home.html", context)


@login_required
@permission_required("publicwork.view_publicworkgroup")
def group_detail(request, pk):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "publicwork/groups/elements/seeker_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "publicwork/groups/detail.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    clear_session(request, ["search", "frequencies"])
    belongs_center(request, pk, PublicworkGroup)
    pw_group = PublicworkGroup.objects.get(pk=pk)
    object_list = pw_group.members.exclude(
        status__in=("ITD", "RST", "STD")
    ).order_by("name")[_from:_to]
    # add action links
    for item in object_list:
        item.to_detail = (
            reverse("seeker_detail", args=[item.pk]) + f"?pwg={pk}"
        )
        item.del_member = reverse("group_remove_member", args=[pk, item.pk])
        item.local = f"{item.city} ({item.state}-{item.country})"

    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object": pw_group,
        "object_list": object_list,
        "active_members": len(object_list),
        "title": _("group detail"),
        "nav": "info",
        "table_title": "Members",
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.add_publicworkgroup")
def group_create(request):
    if request.method == "POST":
        pw_group_form = GroupForm(request.POST)
        if pw_group_form.is_valid():
            pw_group_form.save()
            message = f"The Group '{request.POST['name']}' has been created!"

            messages.success(request, message)
            return redirect(reverse("group_home") + "?init=on")

    context = {
        "form": GroupForm(
            initial={
                "made_by": request.user,
                "center": request.user.person.center,
            }
        ),
        "form_name": "Group",
        "form_path": "publicwork/forms/group.html",
        "goback": reverse("group_home"),
        "title": _("create goup"),
        "to_create": True,
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("publicwork.change_publicworkgroup")
def group_update(request, pk):
    belongs_center(request, pk, PublicworkGroup)

    pw_group = PublicworkGroup.objects.get(pk=pk)
    if request.method == "POST":
        pw_group_form = GroupForm(request.POST, instance=pw_group)
        if pw_group_form.is_valid():
            pw_group_form.save()
            message = f"The Group '{request.POST['name']}' has been updated!"
            messages.success(request, message)

        return redirect("group_detail", pk=pk)

    pw_group_form = GroupForm(
        instance=pw_group,
        initial={"made_by": request.user},
    )

    context = {
        "form": pw_group_form,
        "form_name": "Group",
        "form_path": "publicwork/forms/group.html",
        "goback": reverse("group_detail", args=[pk]),
        "title": _("update group"),
        "pk": pk,
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("publicwork.delete_publicworkgroup")
def group_delete(request, pk):
    pw_group = PublicworkGroup.objects.get(pk=pk)
    if request.method == "POST":
        if pw_group.members.count() > 0 or pw_group.mentors.count() > 0:
            pw_group.is_active = False
            pw_group.save()
        else:
            pw_group.delete()
        return redirect(reverse("group_home") + "?init=on")

    context = {
        "object": pw_group,
        "title": _("confirm to delete"),
    }
    return render(request, "base/confirm_delete.html", context)


@login_required
@permission_required("publicwork.add_publicworkgroup")
def group_reinsert(request, pk):
    pw_group = PublicworkGroup.objects.get(pk=pk)
    if request.method == "POST":
        pw_group.is_active = True
        pw_group.save()
        return redirect(reverse("group_home") + "?init=on")

    context = {
        "object": pw_group,
        "title": _("confirm to reinsert"),
    }
    return render(
        request, "publicwork/seeker/confirm_to_reinsert.html", context
    )


# seeker frequencies
@login_required
@permission_required("publicwork.view_publicworkgroup")
def group_frequencies(request, pk):
    clear_session(request, ["search", "frequencies"])
    belongs_center(request, pk, PublicworkGroup)
    page = request.GET["page"] if request.GET.get("page") else 1

    pw_group = PublicworkGroup.objects.get(pk=pk)
    active_members = pw_group.members.exclude(status__in=("ITD", "RST", "STD"))
    frequencies = get_frequencies([mbr.id for mbr in active_members])

    context = {
        "object": pw_group,
        "title": _("group detail | frequencies"),
        "object_list": paginator(
            sorted(frequencies, key=lambda x: x["rank"], reverse=True),
            20,
            page=page,
        ),
        "active_members": len(active_members),
        "nav": "frequencies",
        "now": datetime.now().date(),
    }

    return render(request, "publicwork/groups/detail.html", context)


# handlers
def get_frequencies(ids):
    seekers = Seeker.objects.filter(id__in=ids)
    status = dict(SEEKER_STATUS)
    frequencies = []
    for seek in seekers:
        seeker = {
            "id": seek.id,
            "name": seek.name,
            "is_active": seek.is_active,
            "center": seek.center,
            "status": status[str(seek.status)],
            "date": seek.status_date,
            "rank": 0,
            "freq": 0,
        }
        if seek.listener_set.count():
            for freq in seek.listener_set.all():
                seeker["rank"] += freq.ranking
                seeker["freq"] += 1
        frequencies.append(seeker)

    return frequencies


@login_required
@permission_required("publicwork.add_listener")
def group_add_frequencies(request, pk):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "publicwork/groups/elements/lecture_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "publicwork/groups/detail.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    belongs_center(request, pk, PublicworkGroup)
    pw_group = PublicworkGroup.objects.get(pk=pk)

    if request.GET.get("lect_pk"):
        # get lecture
        lecture = Lecture.objects.get(pk=request.GET["lect_pk"])
        # create and prepare frequencies object in session, if necessary
        if not request.session.get("frequencies"):
            request.session["frequencies"] = {
                "lecture": {},
                "listeners": [],
            }
            active_members = [
                m
                for m in pw_group.members.all()
                if m.status not in ("ITD", "STD")
            ]
            preparing_the_session(request, active_members, lecture)

    if request.method == "POST":
        listeners = get_listeners_dict(request)
        if listeners:
            for listener in listeners:
                new_freq = dict(
                    lecture=lecture,
                    seeker_id=listener["id"],
                    ranking=listener["rank"],
                    observations=listener["obs"],
                )
                Listener.objects.create(**new_freq)
        return redirect("group_detail", pk=pk)

    queryset = search_lecture(request, Lecture)
    object_list = queryset[_from:_to]
    # add action links
    for item in object_list:
        item.add_freqs_link = (
            reverse("group_add_frequencies", args=[pk]) + f"?lect_pk={item.pk}"
        )

    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object": pw_group,
        "object_list": object_list,
        "title": _("add frequencies"),
        "nav": "add_frequencies",
        "goback": reverse("group_detail", args=[pk]),
        "type_list": LECTURE_TYPES,
        "pk": pk,
    }
    return render(request, template_name, context)


# add member
@login_required
@permission_required("publicwork.change_publicworkgroup")
def group_add_member(request, pk):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "publicwork/groups/elements/seeker_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "publicwork/groups/detail.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    object_list = None
    belongs_center(request, pk, PublicworkGroup)
    pw_group = PublicworkGroup.objects.get(pk=pk)

    if request.GET.get("seek_pk"):
        seeker = Seeker.objects.get(pk=request.GET["seek_pk"])

        if request.method == "POST":
            pw_group.members.add(seeker)
            date = timezone.now().date()
            if seeker.status != "MBR":
                HistoricOfSeeker.objects.create(
                    seeker=seeker,
                    occurrence="MBR",
                    date=date,
                    description=f"Entered in '{pw_group}' group.",
                )
            seeker.status = "MBR"
            seeker.status_date = date
            seeker.save()
            messages.success(request, "The member has been inserted on group!")
            return redirect("group_detail", pk=pk)

        context = {
            "member": seeker.name,
            "insert_to": f"{pw_group.name} {pw_group.center}",
            "title": _("confirm to insert"),
        }
        return render(
            request,
            "publicwork/groups/confirm_add_member_or_mentor.html",
            context,
        )

    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset = search_seeker(request, Seeker)
        object_list = queryset[_from:_to]
        # add action links
        for item in object_list:
            item.add_in_group = reverse("group_add_member", args=[pk])
            item.local = f"{item.city} ({item.state}-{item.country})"

    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object": pw_group,
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("group_add_member", args=[pw_group.pk]),
        "status_list": SEEKER_STATUS,
        "title": _("group add member"),
        "nav": "add_member",
        "goback": reverse("group_detail", args=[pk]),
        "centers": [[str(cnt.pk), str(cnt)] for cnt in Center.objects.all()],
        "user_center": str(request.user.person.center.pk),
        "pk": pk,
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.change_publicworkgroup")
def group_remove_member(request, group_pk, member_pk):
    pw_group = PublicworkGroup.objects.get(pk=group_pk)
    member = Seeker.objects.get(pk=member_pk)

    if request.method == "POST":
        pw_group.members.remove(member)
        return redirect("group_detail", pk=group_pk)

    context = {
        "member": member.name,
        "group": pw_group,
        "title": _("confirm to remove"),
    }
    return render(
        request, "publicwork/groups/confirm_remove_member.html", context
    )


# add mentor
@login_required
@permission_required("publicwork.change_publicworkgroup")
def group_add_mentor(request, pk):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "publicwork/elements/person_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "publicwork/groups/detail.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    object_list = None
    belongs_center(request, pk, PublicworkGroup)
    pw_group = PublicworkGroup.objects.get(pk=pk)

    if request.GET.get("person_pk"):
        person = Person.objects.get(pk=request.GET["person_pk"])

        if request.method == "POST":
            pw_group.mentors.add(person)
            messages.success(
                request, _("The mentor has been inserted on group!")
            )
            return redirect("group_detail", pk=pk)

        context = {
            "member": person.name,
            "insert_to": f"{pw_group.name} {pw_group.center}",
            "title": _("confirm to insert"),
        }
        return render(
            request,
            "publicwork/groups/confirm_add_member_or_mentor.html",
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
                reverse("group_add_mentor", args=[pk])
                + f"?person_pk={ item.pk }"
            )
            item.local = "{} ({}-{})".format(
                item.user.profile.city,
                item.user.profile.state,
                item.user.profile.country,
            )

    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object": pw_group,
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("group_add_mentor", args=[pw_group.pk]),
        "aspect_list": ASPECTS,
        "status_list": STATUS,
        "title": _("group add mentor"),
        "nav": "add_mentor",
        "goback": reverse("group_detail", args=[pk]),
        "pk": pk,
        "flag": "group",
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.change_publicworkgroup")
def group_remove_mentor(request, group_pk, mentor_pk):
    pw_group = PublicworkGroup.objects.get(pk=group_pk)
    mentor = Person.objects.get(pk=mentor_pk)

    if request.method == "POST":
        pw_group.mentors.remove(mentor)
        return redirect("group_detail", pk=group_pk)

    context = {
        "member": mentor.name,
        "group": pw_group,
        "title": _("confirm to remove"),
    }
    return render(
        request, "publicwork/groups/confirm_remove_member.html", context
    )


# handlers
def preparing_the_session(request, members, lecture):
    # check which frequencies have already been entered
    inserteds = [
        [str(lect.seeker.pk), lect.ranking, lect.observations]
        for lect in lecture.listener_set.all()
    ]
    inserteds_pks = [ins[0] for ins in inserteds]
    # adjust frequencies on session
    frequencies = request.session["frequencies"]
    # add lecture
    frequencies["lecture"] = {
        "id": str(lecture.pk),
        "date": str(datetime.strftime(lecture.date, "%d/%m/%Y")),
        "theme": lecture.theme,
        "type": lecture.type,
        "center": str(lecture.center),
    }
    # add frequencies
    frequencies["listeners"] = []
    for seek in members:
        if str(seek.pk) in inserteds_pks:
            for ins in inserteds:
                if str(seek.pk) == ins[0]:
                    listener = {
                        "seeker": {
                            "id": str(seek.pk),
                            "name": seek.short_name,
                            "center": str(seek.center),
                        },
                        "freq": "on",
                        "ranking": ins[1],
                        "observations": ins[2],
                    }
                    break
        else:
            listener = {
                "seeker": {
                    "id": str(seek.pk),
                    "name": seek.short_name,
                    "center": str(seek.center),
                },
                "freq": "",
                "ranking": 0,
                "observations": "",
            }
        frequencies["listeners"].append(listener)
    # save session
    request.session.modified = True


def get_listeners_dict(request):
    from_post = [
        obj for obj in request.POST.items() if obj[0] != "csrfmiddlewaretoken"
    ]
    listeners = []
    for i in range(1, len(request.session["frequencies"]["listeners"]) + 1):
        listener = {}
        for _lis in from_post:
            lis = _lis[0].split("-")
            if lis[1] == str(i):
                listener[lis[0]] = _lis[1]
        if "freq" in listener.keys():
            listeners.append(listener)
    return listeners
