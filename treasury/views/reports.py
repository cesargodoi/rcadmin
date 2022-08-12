from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext as _

from person.models import Person
from rcadmin.common import paginator

from .useful import OrderByPeriod, OrderToJson


def hx_get_order(request):
    template_name = "treasury/elements/hx/modal_order_info_hx.html"
    context = {"order_info": OrderToJson(request.GET.get("order_id"))}
    return render(request, template_name, context)


@login_required
@permission_required("treasury.view_order")
def treasury_home(request):
    template_name = "treasury/home.html"
    # clear session
    if request.session.get("order"):
        del request.session["order"]
    if request.session.get("search"):
        del request.session["search"]
    # create an object list
    object_list = OrderByPeriod(
        request,
        timezone.now().date() - timedelta(30),
        timezone.now().date(),
    )

    last_payments, last_payments_total = object_list.summary("concluded")
    self_payed, self_payed_total = object_list.summary("self_payed")

    context = {
        "last_payments": last_payments,
        "last_payments_total": last_payments_total,
        "self_payed": len(self_payed),
        "self_payed_total": self_payed_total,
        "title": _("treasury"),
        "nav": "home",
    }
    return render(request, template_name, context)


@login_required
@permission_required("treasury.view_order")
def cash_balance(request):
    template_name = "treasury/reports/cash_balance.html"
    search = search_dates(request)
    dt1 = (
        datetime.strptime(request.GET["dt1"], "%Y-%m-%d")
        if request.GET.get("dt1")
        else datetime.strptime(search["dt1"], "%Y-%m-%d")
    )
    search["dt1"] = dt1.strftime("%Y-%m-%d")
    dt2 = (
        datetime.strptime(request.GET["dt2"], "%Y-%m-%d")
        if request.GET.get("dt2")
        else datetime.strptime(search["dt2"], "%Y-%m-%d")
    )
    search["dt2"] = dt2.strftime("%Y-%m-%d")
    # get an object list
    object_list = OrderByPeriod(request, dt1, dt2)
    last_payments, last_payments_total = object_list.summary("concluded")

    context = {
        "last_payments": last_payments,
        "last_payments_total": last_payments_total,
        "period": "from {} to {}".format(
            dt1.strftime("%d/%m/%y"), dt2.strftime("%d/%m/%y")
        ),
        "object_list": object_list.all_payforms,
        "title": _("Cash Balance"),
    }
    return render(request, template_name, context)


@login_required
@permission_required("treasury.view_order")
def period_payments(request):
    template_name = "treasury/reports/period_payments.html"
    search = search_dates(request)
    dt1 = (
        datetime.strptime(request.GET["dt1"], "%Y-%m-%d")
        if request.GET.get("dt1")
        else datetime.strptime(search["dt1"], "%Y-%m-%d")
    )
    search["dt1"] = dt1.strftime("%Y-%m-%d")
    dt2 = (
        datetime.strptime(request.GET["dt2"], "%Y-%m-%d")
        if request.GET.get("dt2")
        else datetime.strptime(search["dt2"], "%Y-%m-%d")
    )
    search["dt2"] = dt2.strftime("%Y-%m-%d")
    # get an object list
    object_list = OrderByPeriod(request, dt1, dt2)
    payments, payments_total = object_list.summary_of_payments()

    context = {
        "last_payments": payments,
        "last_payments_total": payments_total,
        "period": "from {} to {}".format(
            dt1.strftime("%d/%m/%y"), dt2.strftime("%d/%m/%y")
        ),
        "object_list": object_list.all_payments,
        "title": _("Period payments"),
    }
    return render(request, template_name, context)


@login_required
@permission_required("treasury.view_order")
def payments_by_person(request):
    template_name = "treasury/reports/payments_by_person.html"
    if not request.session.get("order"):
        request.session["order"] = {
            "person": {},
            "payments": [],
            "payforms": [],
            "total_payments": 0.0,
            "total_payforms": 0.0,
            "missing": 0.0,
            "status": None,
            "description": "",
            "self_payed": False,
        }

    person = None
    object_list = []

    if request.GET.get("person"):
        person = Person.objects.get(name=request.GET.get("person"))
        request.session["order"]["person"] = {
            "name": person.name,
            "id": str(person.id),
        }
        request.session.modified = True
        payments = person.payment_set.all().order_by("-created_on")
        object_list = paginator(payments, page=request.GET.get("page"))
    elif request.session["order"]["person"]:
        person = Person.objects.get(
            id=request.session["order"]["person"]["id"]
        )
        payments = person.payment_set.all().order_by("-created_on")

        object_list = paginator(payments, page=request.GET.get("page"))

    context = {
        "title": _("Payment by person"),
        "object": person,
        "object_list": object_list,
        "nav": "reports",
    }
    return render(request, template_name, context)


# @login_required
# @permission_required("treasury.view_order")
# def payments_by_person(request):
#     template_name = "treasury/reports/payments_by_person.html"
#     if not request.session.get("order"):
#         request.session["order"] = {
#             "person": {},
#             "payments": [],
#             "payforms": [],
#             "total_payments": 0.0,
#             "total_payforms": 0.0,
#             "missing": 0.0,
#             "status": None,
#             "description": "",
#             "self_payed": False,
#         }

#     person = None
#     object_list = []

#     if request.GET.get("person"):
#         person = Person.objects.get(name=request.GET.get("person"))
#         request.session["order"]["person"] = {
#             "name": person.name,
#             "id": str(person.id),
#         }
#         request.session.modified = True
#         payments = person.payment_set.all().order_by("-created_on")
#         object_list = paginator(payments, page=request.GET.get("page"))
#     elif request.session["order"]["person"]:
#         person = Person.objects.get(
#             id=request.session["order"]["person"]["id"]
#         )
#         payments = person.payment_set.all().order_by("-created_on")

#         object_list = paginator(payments, page=request.GET.get("page"))

#     context = {
#         "title": _("Payment by person"),
#         "object": person,
#         "object_list": object_list,
#         "nav": "reports",
#     }
#     return render(request, template_name, context)


# helpers
# get person by jQuery
def reports_search_person(request):
    template_name = "treasury/reports/payment_by_person.html"
    if request.is_ajax():
        term = request.GET.get("term")
        persons = Person.objects.filter(
            name__icontains=term, center=request.user.person.center
        )[:20]
        results = [person.name for person in persons]
        return JsonResponse(results, safe=False)

    return render(request, template_name)


# search dates
def search_dates(request):
    if not request.session.get("search"):
        request.session["search"] = {
            "dt1": (timezone.now().date() - timedelta(30)).strftime(
                "%Y-%m-%d"
            ),
            "dt2": timezone.now().date().strftime("%Y-%m-%d"),
        }
    return request.session["search"]
