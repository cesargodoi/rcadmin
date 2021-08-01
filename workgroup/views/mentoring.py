from datetime import datetime, date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from schooladmin.common import ACTIVITY_TYPES, paginator, clear_session
from base.searchs import search_event

from person.models import Person
from event.models import Event, Frequency
from ..forms import MentoringFrequencyForm
from ..models import Workgroup, Membership


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_home(request):
    groups = Membership.objects.filter(
        person=request.user.person, role_type="MTR"
    )
    context = {"groups": groups, "title": "mentoring", "nav": "home"}
    return render(request, "workgroup/mentoring/home.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_group_detail(request, pk):
    if request.session.get("frequencies"):
        del request.session["frequencies"]

    workgroup = Workgroup.objects.get(pk=pk)

    queryset = workgroup.membership_set.all().order_by("person__name_sa")

    object_list = paginator(queryset, 25, request.GET.get("page"))
    # add action links
    for member in object_list:
        member.click_link = reverse(
            "mentoring_member_detail", args=[pk, member.person.pk]
        )

    context = {
        "object": workgroup,
        "object_list": object_list,
        "title": "workgroup detail",
        "nav": "detail",
        "tab": "members",
        "goback": reverse("mentoring_home"),
    }
    return render(request, "workgroup/mentoring/group_detail.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_member_detail(request, group_pk, person_pk):
    object = Person.objects.get(pk=person_pk)
    age = (date.today() - object.birth).days // 365
    context = {
        "object": object,
        "title": "member detail",
        "nav": "detail",
        "tab": "info",
        "age": age,
        "goback": reverse("mentoring_group_detail", args=[group_pk]),
        "group_pk": group_pk,
    }
    return render(request, "workgroup/mentoring/member_detail.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_member_frequencies(request, group_pk, person_pk):
    object = Person.objects.get(pk=person_pk)
    page = request.GET["page"] if request.GET.get("page") else 1
    object_list = object.frequency_set.all().order_by("-event__date")
    ranking = sum([f.ranking for f in object_list])
    context = {
        "object": object,
        "title": "member detail | frequencies",
        "object_list": paginator(object_list, page=page),
        "nav": "detail",
        "tab": "frequencies",
        "ranking": ranking,
        "goback": reverse("mentoring_group_detail", args=[group_pk]),
        "group_pk": group_pk,
    }
    return render(request, "workgroup/mentoring/member_detail.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_member_historic(request, group_pk, person_pk):
    object = Person.objects.get(pk=person_pk)
    page = request.GET["page"] if request.GET.get("page") else 1
    object_list = object.historic_set.all().order_by("-date")
    context = {
        "object": object,
        "title": "member detail | historic",
        "object_list": paginator(object_list, page=page),
        "nav": "detail",
        "tab": "historic",
        "goback": reverse("mentoring_group_detail", args=[group_pk]),
        "group_pk": group_pk,
    }
    return render(request, "workgroup/mentoring/member_detail.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def membership_add_frequency(request, group_pk, person_pk):
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
            messages.success(request, "The frequency has been inserted!")
            return redirect(
                "mentoring_member_frequencies",
                group_pk=group_pk,
                person_pk=person_pk,
            )

        context = {
            "object": person,
            "form": MentoringFrequencyForm,
            "insert_to": f"{event.activity.name} {event.center}",
            "title": "confirm to insert",
        }
        return render(
            request, "workgroup/elements/confirm_add_frequency.html", context
        )

    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset, page = search_event(request, Event)
        object_list = paginator(queryset, page=page)
        # add action links
        for member in object_list:
            member.add_link = reverse(
                "membership_add_frequency", args=[group_pk, person_pk]
            )

    context = {
        "object": person,
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "title": "insert frequencies",
        "type_list": ACTIVITY_TYPES,
        "pre_freqs": [obj.event.pk for obj in person.frequency_set.all()],
        "group_pk": group_pk,
    }
    return render(
        request, "workgroup/mentoring/member_add_frequency.html", context
    )


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
        messages.success(request, "The frequency has been updated!")
        return redirect(
            "mentoring_member_frequencies",
            group_pk=group_pk,
            person_pk=person_pk,
        )

    context = {
        "object": person,
        "event": frequency.event,
        "form": MentoringFrequencyForm(instance=frequency),
        "title": "update frequency | person side",
        "goback": reverse(
            "mentoring_member_frequencies", args=[group_pk, person_pk]
        ),
    }
    return render(
        request, "workgroup/mentoring/update_frequency.html", context
    )


@login_required
@permission_required("workgroup.view_workgroup")
def membership_remove_frequency(request, group_pk, person_pk, freq_pk):
    frequency = Frequency.objects.get(pk=freq_pk)

    if request.method == "POST":
        frequency.delete()
        messages.success(request, "The frequency has been removed!")
        return redirect(
            "mentoring_member_frequencies",
            group_pk=group_pk,
            person_pk=person_pk,
        )

    context = {"object": frequency, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)


@login_required
@permission_required("workgroup.view_workgroup")
def mentoring_add_frequencies(request, group_pk):
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
            preparing_the_session(request, workgroup.members.all(), event)

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
        queryset, page = search_event(request, Event)
        object_list = paginator(queryset, page=page)

    context = {
        "object": workgroup,
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "goback_link": reverse("group_detail", args=[group_pk]),
        "title": "workgroup add members",
        "nav": "detail",
        "tab": "add_frequencies",
        "goback": reverse("mentoring_group_detail", args=[group_pk]),
        "group_pk": group_pk,
    }
    return render(request, "workgroup/mentoring/group_detail.html", context)


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
