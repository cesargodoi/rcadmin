from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone


#  center  ####################################################################
def search_center(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        get_base_search(request)
    adjust_session(request, ["ct_term", "page", "all"])
    # basic query
    search = request.session["search"]
    _query = [Q(is_active=True)]
    # adding more complexity
    if search["ct_term"]:
        _query.append(Q(name__icontains=search["ct_term"]))
    if search["all"] == "on":
        _query.remove(Q(is_active=True))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("name"), search["page"])


#  person  ####################################################################
def search_person(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        get_base_search(request)
    adjust_session(
        request, ["ps_term", "ps_aspect", "ps_status", "page", "all"]
    )
    # basic query
    search = request.session["search"]
    _query = [Q(is_active=True), Q(center=request.user.person.center)]
    # adding more complexity
    if search["ps_term"]:
        _query.append(Q(name_sa__icontains=search["ps_term"]))
    if search["ps_aspect"] != "all":
        _query.append(Q(aspect=search["ps_aspect"]))
    if search["ps_status"] != "all":
        _query.append(Q(status=search["ps_status"]))
        if search["ps_status"] in ["DIS", "REM", "DEA"]:
            _query.remove(Q(is_active=True))
    if search["all"] == "on":
        _query.remove(Q(is_active=True))
        _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("name_sa"), search["page"])


#  event  ####################################################################
def search_event(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        get_base_search(request)
    adjust_session(request, ["dt1", "dt2", "ev_type", "page", "all"])
    # basic query
    search = request.session["search"]
    _query = [
        Q(is_active=True),
        Q(center=request.user.person.center),
        Q(date__range=[search["dt1"], search["dt2"]]),
    ]
    # adding more complexity
    if search["ev_type"] != "all":
        _query.append(Q(activity__activity_type=search["ev_type"]))
    if search["all"] == "on":
        _query.remove(Q(is_active=True))
        _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("-date"), search["page"])


#  workgroups  ################################################################
def search_workgroup(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        get_base_search(request)
    adjust_session(request, ["wg_term", "wg_type", "page", "all"])
    # basic query
    search = request.session["search"]
    _query = [Q(is_active=True), Q(center=request.user.person.center)]
    # adding more complexity
    if search["wg_term"]:
        _query.append(Q(name__icontains=search["wg_term"]))
    if search["wg_type"] != "all":
        _query.append(Q(workgroup_type=search["wg_type"]))
    if search["all"] == "on":
        _query.remove(Q(is_active=True))
        _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("name"), search["page"])


#  seeker  ####################################################################
def search_seeker(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        get_base_search(request)
    adjust_session(
        request, ["sk_name", "sk_city", "sk_status", "center", "page", "all"]
    )
    # basic query
    search = request.session["search"]
    _query = [Q(is_active=True), Q(center=request.user.person.center)]
    # adding more complexity
    if search["sk_name"]:
        _query.append(Q(name_sa__icontains=search["sk_name"]))
    if search["sk_city"]:
        _query.append(Q(city__icontains=search["sk_city"]))
    if search["sk_status"] != "all":
        _query.append(Q(status=search["sk_status"]))
    if search["center"]:
        _query.remove(Q(center=request.user.person.center))
        _query.append(Q(center__pk=search["center"]))
    if search["all"] == "on":
        _query.remove(Q(is_active=True))
        if Q(center=request.user.person.center) in _query:
            _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("name_sa"), search["page"])


#  lecture  ###################################################################
def search_lecture(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        get_base_search(request)
    adjust_session(request, ["dt1", "dt2", "lc_type", "page", "all"])
    # basic query
    search = request.session["search"]
    _query = [
        Q(is_active=True),
        Q(center=request.user.person.center),
        Q(date__range=[search["dt1"], search["dt2"]]),
    ]
    # adding more complexity
    if search["lc_type"] != "all":
        _query.append(Q(type=search["lc_type"]))
    if search["all"] == "on":
        _query.remove(Q(is_active=True))
        _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("-date"), search["page"])


#  pw group  ##################################################################
def search_pw_group(request, obj):
    # checking for search in request.session
    if not request.session.get("search"):
        get_base_search(request)
    adjust_session(request, ["pw_name", "center", "page", "all"])
    # basic query
    search = request.session["search"]
    _query = [Q(is_active=True), Q(center=request.user.person.center)]
    # adding more complexity
    if search["pw_name"]:
        _query.append(Q(name__icontains=search["pw_name"]))
    if search["center"]:
        _query.remove(Q(center=request.user.person.center))
        _query.append(Q(center__pk=search["center"]))
    if search["all"] == "on":
        _query.remove(Q(is_active=True))
        if Q(center=request.user.person.center) in _query:
            _query.remove(Q(center=request.user.person.center))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("name"), search["page"])


#  orders  ####################################################################
def search_order(request, obj):
    if not request.session.get("search"):
        get_base_search(request)
    adjust_session(request, ["dt1", "dt2", "od_name", "od_status", "page"])
    # basic query
    search = request.session["search"]
    # basic query
    _query = [
        Q(center=request.user.person.center),
        Q(created_on__date__range=[search["dt1"], search["dt2"]]),
    ]
    # adding more complexity
    if search["od_name"]:
        _query.append(Q(person__name_sa__icontains=search["od_name"]))
    if search["od_status"] != "all":
        _query.append(Q(status=search["od_status"]))
    # generating query
    query = Q()
    for q in _query:
        query.add(q, Q.AND)

    return (obj.objects.filter(query).order_by("-created_on"), search["page"])


#  handlers  ##################################################################
def get_base_search(request):
    request.session["search"] = {
        "ct_term": "",
        "ps_term": "",
        "wg_term": "",
        "sk_name": "",
        "sk_city": "",
        "pw_name": "",
        "od_name": "",
        "ps_aspect": "all",
        "od_status": "all",
        "sk_status": "all",
        "ps_status": "all",
        "dt1": (timezone.now() - timedelta(30)).strftime("%Y-%m-%d"),
        "dt2": timezone.now().strftime("%Y-%m-%d"),
        "ev_type": "all",
        "lc_type": "all",
        "wg_type": "all",
        "center": "",
        "page": 1,
        "all": "off",
    }


def get_date(request, dtx, days=0):
    date = (
        datetime.strptime(request.GET[dtx], "%Y-%m-%d")
        if request.GET.get(dtx)
        # else timezone.now() - timedelta(days)
        else datetime.strptime(request.session["search"][dtx], "%Y-%m-%d")
    )
    return date.strftime("%Y-%m-%d")


def adjust_session(request, fields):
    search = request.session["search"]
    for field in fields:
        if field == "all":
            if request.GET.get(field) == "on":
                search[field] = request.GET[field]
            if request.GET.get(field) == "off":
                search[field] = request.GET[field]
        elif field in ["dt1", "dt2", "dt", "date"]:
            search[field] = (
                get_date(request, "dt1", days=30)
                if field == "dt1"
                else get_date(request, "dt2")
            )
        else:
            if request.GET.get(field):
                search[field] = request.GET[field]
    # save session
    request.session.modified = True
