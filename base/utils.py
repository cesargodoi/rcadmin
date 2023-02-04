from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone


#  person - reports  ##########################################################
def get_installed_per_period_dict(request, obj):
    put_search_in_session(request)
    search = request.session["search"]
    get_period(request, search)
    request.session.modified = True
    # basic query
    _query = [
        Q(is_active=True),
        Q(center=request.user.person.center),
        Q(aspect="A1"),
        Q(aspect_date__range=[search["dt1"], search["dt2"]]),
    ]
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    _dict = []
    for _obj in obj.objects.filter(query).order_by("-aspect_date"):
        row = dict(
            pk=_obj.pk,
            name=_obj.short_name,
            local=f"{_obj.user.profile.city} ({_obj.user.profile.state})",
            status=_obj.get_status_display(),
            aspect=_obj.get_aspect_display(),
            date=_obj.aspect_date,
        )
        _dict.append(row)
    return _dict


def get_occurrences_per_period_dict(request, obj):
    put_search_in_session(request)
    search = request.session["search"]
    get_period(request, search)
    request.session.modified = True
    # basic query
    _query = [
        Q(person__center=request.user.person.center),
        Q(date__range=[search["dt1"], search["dt2"]]),
    ]
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    _dict = []
    for _obj in obj.objects.filter(query).order_by("-date"):
        row = dict(
            pk=_obj.pk,
            name=_obj.person.short_name,
            local="{} ({})".format(
                _obj.person.user.profile.city, _obj.person.user.profile.state
            ),
            occurrence=_obj.get_occurrence_display(),
            description=_obj.description,
            date=_obj.date,
        )
        _dict.append(row)
    return _dict


#  publicwork - reports  ######################################################
def get_lectures_dict(request, obj):
    _dict = []
    for obj in queryset_per_date(request, obj):
        row = dict(
            pk=obj.pk,
            date=obj.date,
            theme=obj.theme,
            type=str(obj.get_type_display()),
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
                        obs=freq.observations,
                        lect_pk=freq.lecture.pk,
                        lect_theme=freq.lecture.theme,
                        lect_type=str(obj.get_type_display()),
                        lect_date=freq.lecture.date,
                        lect_center=str(freq.lecture.center),
                        seek_pk=freq.seeker.pk,
                        seek_name=freq.seeker.short_name,
                        seek_birth=freq.seeker.birth,
                        seek_gender=freq.seeker.gender,
                        seek_city=freq.seeker.city,
                        seek_state=freq.seeker.state,
                        seek_country=freq.seeker.country,
                        seek_local=f"{freq.seeker.city} ({freq.seeker.state})",
                        seek_center=str(freq.seeker.center),
                        seek_status=str(freq.seeker.get_status_display()),
                        seek_status_date=freq.seeker.status_date,
                        seek_is_active=freq.seeker.is_active,
                    )
                _dict.append(row)
    return _dict


def get_seekers_dict(request, obj):
    put_search_in_session(request)
    search = request.session["search"]
    search["status"] = (
        request.GET["status"] if request.GET.get("status") else ""
    )
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

    _dict = []
    for obj in obj.objects.filter(query).order_by("name_sa"):
        if obj.is_active:
            row = dict(
                pk=obj.pk,
                name=obj.short_name,
                birth=obj.birth,
                gender=obj.gender,
                city=obj.city,
                state=obj.state,
                country=obj.country,
                local=f"{obj.city} ({obj.state})",
                center=str(obj.center),
                status=obj.get_status_display(),
                status_date=obj.status_date,
            )
        _dict.append(row)
    return _dict


# helpers #####################################################################
def queryset_per_date(request, obj):
    put_search_in_session(request)
    search = request.session["search"]
    get_period(request, search)
    search["all"] = "on" if request.GET.get("all") else ""
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


def get_period_subtitle(request):
    return "from: {0} to: {1}".format(
        datetime.strftime(
            datetime.strptime(request.GET["dt1"], "%Y-%m-%d"),
            "%d/%m/%y",
        ),
        datetime.strftime(
            datetime.strptime(request.GET["dt2"], "%Y-%m-%d"),
            "%d/%m/%y",
        ),
    )


def get_report_file_title(request, report_name):
    if not request.GET.get("dt1") or not request.GET.get("dt1"):
        return "{0} - {1}.xlsx".format(
            "_".join(request.user.person.center.short_name.split()),
            report_name,
        )
    return "{0} - {1} ({2} to {3}).xlsx".format(
        "_".join(request.user.person.center.short_name.split()),
        report_name,
        request.GET["dt1"],
        request.GET["dt2"],
    )


def put_search_in_session(request):
    if not request.session.get("search"):
        request.session["search"] = {}


def get_period(request, search):
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
