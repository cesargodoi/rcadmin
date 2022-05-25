from datetime import datetime, date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import ACTIVITY_TYPES, paginator, clear_session
from base.searchs import search_event

from person.models import Person
from event.models import Event, Frequency
from ..forms import MentoringFrequencyForm
from ..models import Workgroup, Membership


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_home(request):
    object_list = Membership.objects.filter(
        person=request.user.person, role_type="MTR"
    )
    for item in object_list:
        item.click_link = reverse(
            "mentoring_group_detail", args=[item.workgroup.pk]
        )
        mentors = [
            mtr
            for mtr in item.workgroup.membership_set.all()
            if mtr.role_type == "MTR"
        ]
        item.workgroup.mentors = mentors
        item.workgroup.num_members = (
            item.workgroup.membership_set.count() - len(mentors)
        )

    context = {
        "object_list": object_list,
        "title": _("mentoring"),
        "nav": "home",
    }
    return render(request, "workgroup/mentoring/home.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_group_detail(request, pk):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "workgroup/mentoring/elements/person_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "workgroup/mentoring/detail.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    if request.session.get("frequencies"):
        del request.session["frequencies"]

    workgroup = Workgroup.objects.get(pk=pk)

    _members = workgroup.membership_set.all().order_by("person__name_sa")
    mentors = [
        mtr.person.short_name for mtr in _members if mtr.role_type == "MTR"
    ]
    members = [mbr for mbr in _members if mbr.role_type in ("MBR", "CTT")]

    object_list = members[_from:_to]
    # add action links
    for item in object_list:
        item.click_link = reverse(
            "mentoring_member_detail", args=[pk, item.person.pk]
        )
        item.local = "{} ({}-{})".format(
            item.person.user.profile.city,
            item.person.user.profile.state,
            item.person.user.profile.country,
        )

    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object": workgroup,
        "object_list": object_list,
        "mentors": mentors,
        "title": _("workgroup detail"),
        "nav": "detail",
        "tab": "members",
        "goback": reverse("mentoring_home"),
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_group_frequencies(request, pk):
    if request.session.get("frequencies"):
        del request.session["frequencies"]

    workgroup = Workgroup.objects.get(pk=pk)

    _members = workgroup.membership_set.all().order_by("person__name_sa")
    mentors = [
        mtr.person.short_name for mtr in _members if mtr.role_type == "MTR"
    ]
    members = [mbr for mbr in _members if mbr.role_type in ("MBR", "CTT")]

    object_list = paginator(members, 25, request.GET.get("page"))

    # add action links
    for member in object_list:
        member.click_link = reverse(
            "mentoring_member_detail", args=[pk, member.person.pk]
        )
        ranks = [f.ranking for f in member.person.frequency_set.all()]
        member.freq = len(ranks)
        member.rank = sum(ranks)

    context = {
        "object": workgroup,
        "object_list": sorted(object_list, key=lambda x: x.rank, reverse=True),
        "mentors": mentors,
        "title": _("workgroup detail"),
        "nav": "detail",
        "tab": "frequencies",
        "goback": reverse("mentoring_home"),
    }
    return render(request, "workgroup/mentoring/detail.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_member_detail(request, group_pk, person_pk):
    obj = Person.objects.get(pk=person_pk)
    age = (date.today() - obj.birth).days // 365
    context = {
        "object": obj,
        "title": _("member detail"),
        "nav": "detail",
        "tab": "info",
        "age": age,
        "goback": reverse("mentoring_group_detail", args=[group_pk]),
        "group_pk": group_pk,
    }
    return render(request, "workgroup/member/detail.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_member_frequencies(request, group_pk, person_pk):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "workgroup/member/elements/frequency_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "workgroup/member/detail.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    obj = Person.objects.get(pk=person_pk)
    object_list = obj.frequency_set.all().order_by("-event__date")[_from:_to]
    ranking = sum([f.ranking for f in object_list])
    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object": obj,
        "title": _("member detail | frequencies"),
        "object_list": object_list,
        "nav": "detail",
        "tab": "frequencies",
        "ranking": ranking,
        "goback": reverse("mentoring_group_detail", args=[group_pk]),
        "group_pk": group_pk,
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_member_historic(request, group_pk, person_pk):
    obj = Person.objects.get(pk=person_pk)
    page = request.GET["page"] if request.GET.get("page") else 1
    object_list = obj.historic_set.all().order_by("-date")
    context = {
        "object": obj,
        "title": _("member detail | historic"),
        "object_list": paginator(object_list, page=page),
        "nav": "detail",
        "tab": "historic",
        "goback": reverse("mentoring_group_detail", args=[group_pk]),
        "group_pk": group_pk,
    }
    return render(request, "workgroup/member/detail.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def membership_add_frequency(request, group_pk, person_pk):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "workgroup/member/elements/event_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "workgroup/member/add_frequency.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    object_list = None
    person = Person.objects.get(pk=person_pk)

    if request.GET.get("pk"):
        event = Event.objects.get(pk=request.GET.get("pk"))

        if request.method == "POST":
            person.frequency_set.create(
                person=person,
                event=event,
                aspect=person.aspect,
                ranking=request.POST.get("ranking"),
                observations=request.POST.get("observations"),
            )
            messages.success(request, _("The frequency has been inserted!"))
            return redirect(
                "mentoring_member_frequencies",
                group_pk=group_pk,
                person_pk=person_pk,
            )

        context = {
            "object": person,
            "form": MentoringFrequencyForm,
            "insert_to": f"{event.activity.name} {event.center}",
            "title": _("confirm to insert"),
        }
        return render(
            request, "workgroup/elements/confirm_add_frequency.html", context
        )

    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset, page_ = search_event(request, Event)
        object_list = queryset[_from:_to]
        # add action links
        for member in object_list:
            member.add_link = reverse(
                "membership_add_frequency", args=[group_pk, person_pk]
            )

    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object": person,
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "title": _("insert frequencies"),
        "type_list": ACTIVITY_TYPES,
        "pre_freqs": [obj.event.pk for obj in person.frequency_set.all()],
        "group_pk": group_pk,
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.view_workgroup")
def membership_update_frequency(request, group_pk, person_pk, freq_pk):
    person = Person.objects.get(pk=person_pk)
    frequency = Frequency.objects.get(pk=freq_pk)

    if request.method == "POST":
        frequency.ranking = (
            int(request.POST["ranking"]) if request.POST.get("ranking") else 0
        )
        frequency.observations = request.POST["observations"]
        frequency.save()
        messages.success(request, _("The frequency has been updated!"))
        return redirect(
            "mentoring_member_frequencies",
            group_pk=group_pk,
            person_pk=person_pk,
        )

    context = {
        "object": person,
        "event": frequency.event,
        "form": MentoringFrequencyForm(instance=frequency),
        "title": _("update frequency | person side"),
        "goback": reverse(
            "mentoring_member_frequencies", args=[group_pk, person_pk]
        ),
    }
    return render(request, "workgroup/member/update_frequency.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def membership_remove_frequency(request, group_pk, person_pk, freq_pk):
    frequency = Frequency.objects.get(pk=freq_pk)

    if request.method == "POST":
        frequency.delete()
        messages.success(request, _("The frequency has been removed!"))
        return redirect(
            "mentoring_member_frequencies",
            group_pk=group_pk,
            person_pk=person_pk,
        )

    context = {
        "object": frequency,
        "title": _("confirm to delete"),
    }
    return render(request, "base/confirm_delete.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_add_frequencies(request, group_pk):
    # get page
    regs = 10
    # select template and page of pagination
    if request.htmx:
        template_name = "workgroup/mentoring/elements/event_list.html"
        page = int(request.GET.get("page"))
    else:
        template_name = "workgroup/mentoring/add_frequencies.html"
        page = 1
    # get limitby
    _from, _to = regs * (page - 1), regs * page

    workgroup = Workgroup.objects.get(pk=group_pk)

    if request.GET.get("event_pk"):
        # get event
        event = Event.objects.get(pk=request.GET["event_pk"])
        # create and prepare frequencies object in session, if necessary
        if not request.session.get("frequencies"):
            request.session["frequencies"] = {
                "event": {},
                "listeners": [],
            }
            _members = workgroup.membership_set.all().order_by(
                "person__name_sa"
            )
            members = [
                mbr.person for mbr in _members if mbr.role_type == "MBR"
            ]
            preparing_the_session(request, members, event)

    if request.method == "POST":
        listeners = get_listeners_dict(request)
        if listeners:
            for listener in listeners:
                new_freq = dict(
                    event=event,
                    person_id=listener["id"],
                    aspect=listener["asp"],
                    ranking=listener["rank"],
                    observations=listener["obs"],
                )
                Frequency.objects.create(**new_freq)
        return redirect("mentoring_group_detail", pk=group_pk)

    if request.GET.get("init"):
        clear_session(request, ["search"])
        object_list = None
    else:
        queryset, page_ = search_event(request, Event)
        object_list = queryset[_from:_to]

    mentors = [
        mtr.person.short_name
        for mtr in workgroup.membership_set.all().order_by("person__name_sa")
        if mtr.role_type == "MTR"
    ]

    context = {
        "page": page,
        "counter": (page - 1) * 10,
        "object_list": object_list,
        "object": workgroup,
        "mentors": mentors,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("group_detail", args=[group_pk]),
        "title": _("workgroup add members"),
        "nav": "detail",
        "tab": "add_frequencies",
        "goback": reverse("mentoring_group_detail", args=[group_pk]),
        "group_pk": group_pk,
    }
    return render(request, template_name, context)


# handlers
def preparing_the_session(request, persons, event):
    # check which frequencies have already been entered
    inserteds = [
        [str(ev.person.pk), ev.person.aspect, ev.ranking, ev.observations]
        for ev in event.frequency_set.all()
    ]
    inserteds_pks = [ins[0] for ins in inserteds]
    # adjust frequencies on session
    frequencies = request.session["frequencies"]
    # add event
    frequencies["event"] = {
        "id": str(event.pk),
        "date": str(datetime.strftime(event.date, "%d/%m/%Y")),
        "name": event.activity.name,
        "center": str(event.center),
    }
    # add listeners
    frequencies["listeners"] = []
    for per in persons:
        if str(per.pk) in inserteds_pks:
            for ins in inserteds:
                if str(per.pk) == ins[0]:
                    listener = {
                        "person": {
                            "id": str(per.pk),
                            "name": per.short_name,
                            "center": str(per.center),
                        },
                        "frequency": "on",
                        "aspect": ins[1],
                        "ranking": ins[2],
                        "observations": ins[3],
                    }
                    break
        else:
            listener = {
                "person": {
                    "id": str(per.pk),
                    "name": per.short_name,
                    "center": str(per.center),
                },
                "frequency": "",
                "aspect": per.aspect,
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
