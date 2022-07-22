from datetime import datetime, date

from django.http import QueryDict
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import (
    ACTIVITY_TYPES,
    clear_session,
    get_template_and_pagination,
)
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
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "workgroup/mentoring/detail.html",
        "workgroup/mentoring/elements/person_list.html",
    )

    if request.session.get("frequencies"):
        del request.session["frequencies"]

    workgroup = Workgroup.objects.get(pk=pk)

    _members = workgroup.membership_set.all().order_by("person__name_sa")
    mentors = [
        mtr.person.short_name for mtr in _members if mtr.role_type == "MTR"
    ]
    count = len([mbr for mbr in _members if mbr.role_type in ("MBR", "CTT")])
    object_list = [mbr for mbr in _members if mbr.role_type in ("MBR", "CTT")][
        _from:_to
    ]

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
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": workgroup,
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
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "workgroup/mentoring/detail.html",
        "workgroup/mentoring/elements/frequency_list.html",
    )

    if request.session.get("frequencies"):
        del request.session["frequencies"]

    workgroup = Workgroup.objects.get(pk=pk)

    _members = workgroup.membership_set.all().order_by("person__name_sa")
    mentors = [
        mtr.person.short_name for mtr in _members if mtr.role_type == "MTR"
    ]
    members = [mbr for mbr in _members if mbr.role_type in ("MBR", "CTT")]

    count = len(members)
    object_list = members[_from:_to]

    # add action links
    for member in object_list:
        member.click_link = reverse(
            "mentoring_member_detail", args=[pk, member.person.pk]
        )
        ranks = [f.ranking for f in member.person.frequency_set.all()]
        member.freq = len(ranks)
        member.rank = sum(ranks)

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": workgroup,
        "mentors": mentors,
        "title": _("workgroup detail"),
        "nav": "detail",
        "tab": "frequencies",
        "goback": reverse("mentoring_home"),
    }
    return render(request, template_name, context)


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
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "workgroup/member/detail.html",
        "workgroup/member/elements/frequency_list.html",
    )

    obj = Person.objects.get(pk=person_pk)
    count = obj.frequency_set.all().count()
    object_list = obj.frequency_set.all().order_by("-event__date")[_from:_to]
    ranking = sum([f.ranking for f in object_list])

    # add action links
    for item in object_list:
        item.update_link = reverse(
            "membership_update_frequency", args=[group_pk, person_pk, item.pk]
        )
        item.del_link = reverse(
            "membership_remove_frequency", args=[group_pk, person_pk, item.pk]
        )

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": obj,
        "title": _("member detail | frequencies"),
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
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "workgroup/member/detail.html",
        "workgroup/member/elements/historic_list.html",
    )

    obj = Person.objects.get(pk=person_pk)
    page = request.GET["page"] if request.GET.get("page") else 1
    count = obj.historic_set.all().count()
    object_list = obj.historic_set.all().order_by("-date")[_from:_to]

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": obj,
        "title": _("member detail | historic"),
        "nav": "detail",
        "tab": "historic",
        "goback": reverse("mentoring_group_detail", args=[group_pk]),
        "group_pk": group_pk,
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.view_workgroup")
def membership_add_frequency(request, group_pk, person_pk):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "workgroup/member/add_frequency.html",
        "workgroup/member/elements/event_list.html",
    )

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

            return redirect(
                "mentoring_member_frequencies",
                group_pk=group_pk,
                person_pk=person_pk,
            )

        template_name = "workgroup/forms/member_frequency.html"
        context = {
            "person": person.name,
            "event": event,
            "form": MentoringFrequencyForm,
            "callback_link": reverse(
                "membership_add_frequency", args=[group_pk, person_pk]
            )
            + f"?pk={request.GET.get('pk')}",
            "title": _("Confirm to insert"),
        }
        return render(request, template_name, context)

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_event(request, Event, _from, _to)
        # add action links
        for member in object_list:
            member.add_link = reverse(
                "membership_add_frequency", args=[group_pk, person_pk]
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
        "object": person,
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
        data = QueryDict(request.body).dict()
        form = MentoringFrequencyForm(data, instance=frequency)
        if form.is_valid():
            form.save()

            frequency.update_link = reverse(
                "membership_update_frequency",
                args=[group_pk, person_pk, frequency.pk],
            )
            frequency.del_link = reverse(
                "membership_remove_frequency",
                args=[group_pk, person_pk, frequency.pk],
            )

            template_name = (
                "workgroup/member/elements/hx/frequency_updated.html"
            )
            context = {"obj": frequency, "pos": request.GET.get("pos")}
            return render(request, template_name, context)

    template_name = "workgroup/forms/member_frequency.html"
    context = {
        "form": MentoringFrequencyForm(instance=frequency),
        "object": person,
        "event": frequency.event,
        "callback_link": reverse(
            "membership_update_frequency", args=[group_pk, person_pk, freq_pk]
        ),
        "goback": reverse(
            "mentoring_member_frequencies", args=[group_pk, person_pk]
        ),
        "freq_pk": freq_pk,
        "pos": request.GET.get("pos"),
        "title": _("Confirm to update"),
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.view_workgroup")
def membership_remove_frequency(request, group_pk, person_pk, freq_pk):
    frequency = Frequency.objects.get(pk=freq_pk)

    if request.method == "POST":
        frequency.delete()

        return redirect(
            "mentoring_member_frequencies",
            group_pk=group_pk,
            person_pk=person_pk,
        )

    template_name = "workgroup/confirm/delete.html"
    context = {
        "object": "{} ⛔️ {} - {}".format(
            frequency.person.name,
            frequency.event.activity.name,
            frequency.event.center,
        ),
        "del_link": reverse(
            "membership_remove_frequency", args=[group_pk, person_pk, freq_pk]
        ),
    }
    return render(request, template_name, context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_add_frequencies(request, group_pk):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "workgroup/mentoring/add_frequencies.html",
        "workgroup/mentoring/elements/event_list.html",
    )

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
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_event(request, Event, _from, _to)

    mentors = [
        mtr.person.short_name
        for mtr in workgroup.membership_set.all().order_by("person__name_sa")
        if mtr.role_type == "MTR"
    ]

    if not request.htmx and object_list:
        message = f"{count} records were found in the database"
        messages.success(request, message)

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
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
