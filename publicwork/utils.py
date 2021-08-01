from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone
from schooladmin.common import LECTURE_TYPES, SEEKER_STATUS


LECT_TYPES = dict(LECTURE_TYPES)
SEEK_STATUS = dict(SEEKER_STATUS)


# reports
def get_lectures_dict(request, obj):
    _dict = []
    for obj in queryset_per_date(request, obj):
        row = dict(
            pk=obj.pk,
            date=obj.date,
            theme=obj.theme,
            type=LECT_TYPES[obj.type],
            listeners=obj.listener_set.count(),
            center=str(obj.center),
            center_city=obj.center.city,
            center_state=obj.center.state,
            center_country=obj.center.country,
        )
        _dict.append(row)
    return _dict


def get_frequencies_dict(request, obj):
    _dict = []
    for obj in queryset_per_date(request, obj):
        if obj.listener_set.count():
            for freq in obj.listener_set.all():
                if freq.seeker.is_active:
                    row = dict(
                        pk=freq.pk,
                        ranking=freq.ranking,
                        obs=freq.observations,
                        lect_pk=freq.lecture.pk,
                        lect_theme=freq.lecture.theme,
                        lect_type=LECT_TYPES[obj.type],
                        lect_date=freq.lecture.date,
                        lect_center=str(freq.lecture.center),
                        seek_pk=freq.seeker.pk,
                        seek_name=freq.seeker.short_name,
                        seek_birth=freq.seeker.birth,
                        seek_gender=freq.seeker.gender,
                        seek_city=freq.seeker.city,
                        seek_state=freq.seeker.state,
                        seek_country=freq.seeker.country,
                        seek_local="{} ({}-{})".format(
                            freq.seeker.city,
                            freq.seeker.state,
                            freq.seeker.country,
                        ),
                        seek_center=str(freq.seeker.center),
                        seek_status=SEEK_STATUS[freq.seeker.status],
                        seek_status_date=freq.seeker.status_date,
                        seek_is_active=freq.seeker.is_active,
                    )
                _dict.append(row)
    return _dict


def get_seekers_dict(request, obj):
    queryset = queryset_per_status(request, obj)
    _dict = []
    for obj in queryset:
        if obj.is_active:
            row = dict(
                pk=obj.pk,
                name=obj.short_name,
                birth=obj.birth,
                gender=obj.gender,
                city=obj.city,
                state=obj.state,
                country=obj.country,
                local="{} ({}-{})".format(obj.city, obj.state, obj.country),
                center=str(obj.center),
                status=SEEK_STATUS[obj.status],
                status_date=obj.status_date,
            )
        _dict.append(row)
    return _dict


# searchs of reports
def queryset_per_date(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "dt1": "",
            "dt2": "",
            "all": "",
        }
    # adjust search
    search = request.session["search"]
    dt1 = (
        datetime.strptime(request.GET["dt1"], "%Y-%m-%d")
        if request.GET.get("dt1")
        else timezone.now() - timedelta(30)
    )
    search["dt1"] = dt1.strftime("%Y-%m-%d")
    dt2 = (
        datetime.strptime(request.GET["dt2"], "%Y-%m-%d")
        if request.GET.get("dt2")
        else timezone.now()
    )
    search["dt2"] = dt2.strftime("%Y-%m-%d")
    search["all"] = "on" if request.GET.get("all") else ""
    # save session
    request.session.modified = True
    # basic query
    _query = [
        Q(is_active=True),
        Q(center=request.user.person.center),
        Q(date__range=[search["dt1"], search["dt2"]]),
    ]
    # adding more complexity
    if search["all"]:
        _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return obj.objects.filter(query).order_by("-date")


def queryset_per_status(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        request.session["search"] = {
            "status": "",
        }
    # adjust search
    search = request.session["search"]
    search["status"] = (
        request.GET["status"] if request.GET.get("status") else ""
    )
    # save session
    request.session.modified = True
    # basic query
    _query = [Q(is_active=True), Q(center=request.user.person.center)]
    # adding more complexity
    if search["status"] != "all":
        _query.append(Q(status=search["status"]))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return obj.objects.filter(query).order_by("name_sa")
