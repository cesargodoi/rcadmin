from datetime import datetime

from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from event.models import Event
from person.models import Person
from rcadmin.common import (
    ORDER_STATUS,
    PAYFORM_TYPES,
    paginator,
    short_name,
    clear_session,
)
from base.searchs import search_order

from ..forms import FormOfPaymentForm, FormUpdateStatus, PaymentForm
from ..models import BankFlags, Order, PayTypes


@login_required
@permission_required("treasury.view_order")
def orders(request):
    template_name = "treasury/order/home.html"
    object_list = None
    if request.session.get("order"):
        del request.session["order"]
    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset, page = search_order(request, Order)
        object_list = paginator(queryset, 25, page=page)

    context = {
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "status_list": ORDER_STATUS,
        "title": _("Orders"),
        "nav": "order",
    }
    return render(request, template_name, context)


@login_required
@permission_required("treasury.add_order")
def order_create(request):
    if not request.session.get("order"):
        request.session["order"] = {
            "person": {},
            "payments": [],
            "payforms": [],
            "total_payments": 0.0,
            "total_payforms": 0.0,
            "missing": 0.0,
            "status": {"cod": "PND"},
            "description": "",
            "self_payed": False,
        }

    if request.GET.get("person"):
        person = Person.objects.get(name=request.GET.get("person"))
        request.session["order"]["person"] = {
            "name": person.name,
            "id": str(person.id),
        }
        request.session.modified = True

    context = {
        "to_create": True,
        "title": _("Create Order"),
        "status": ORDER_STATUS,
    }
    return render(request, "treasury/order/create.html", context)


@require_http_methods(["GET"])
def search_person_by_name(request):
    template_name = "treasury/order/elements/search_results.html"
    results = (
        Person.objects.filter(
            name__icontains=request.GET.get("term"),
            center=request.user.person.center,
        )[:10]
        if request.GET.get("term")
        else None
    )

    context = {"results": results}
    return render(request, template_name, context)


@require_http_methods(["GET"])
def order_add_person(request):
    _name = request.GET.get("name")
    _id = request.GET.get("id")
    request.session["order"]["person"] = {"name": _name, "id": _id}
    request.session.modified = True
    return HttpResponse(_name)


@login_required
@permission_required("treasury.add_order")
def order_add_payment(request):
    template_name = "treasury/order/elements/payment_add.html"
    if request.method == "POST":
        template_name = "treasury/order/elements/payment.html"

        _ids = (
            [int(i["id"]) for i in request.session["order"]["payments"]]
            if request.session["order"]["payments"]
            else 0
        )
        new = {
            "id": max(_ids) + 1 if _ids else 1,
            "paytype": {},
            "person": {},
            "ref_month": {},
            "event": {},
            "value": 0.0,
            "obs": "",
        }

        if request.POST.get("paytype"):
            paytype = PayTypes.objects.get(id=request.POST.get("paytype"))
            new["paytype"] = {"name": paytype.name, "id": paytype.id}

        if request.POST.get("person"):
            person = Person.objects.get(id=request.POST.get("person"))
            new["person"] = {
                "name": person.short_name,
                "id": str(person.id),
            }

        if request.POST.get("ref_month"):
            ref = request.POST.get("ref_month")
            _repr = datetime.strptime(ref, "%Y-%m-%d").date()
            new["ref_month"] = {"repr": _repr.strftime("%b/%y"), "ref": ref}

        if request.POST.get("event"):
            event = Event.objects.get(id=request.POST.get("event"))
            _event = "{}... {} ({})".format(
                event.activity.name[:4],
                event.center,
                event.date.strftime("%d/%m/%y"),
            )
            new["event"] = {"event": _event, "id": str(event.id)}

        if request.POST.get("value"):
            value = float(request.POST.get("value"))
            new["value"] = value
            request.session["order"]["total_payments"] += value
            request.session["order"]["missing"] += value

        if request.POST.get("obs"):
            new["obs"] = request.POST.get("obs")[:50]

        request.session["order"]["payments"].append(new)
        request.session.modified = True

        context = {"object": new}
        return render(request, template_name, context)

    # change queryset for person field and set current person as initial
    persons = Person.objects.filter(center=request.user.person.center)
    current_person = [
        person
        for person in persons
        if person.name == request.session["order"]["person"]["name"]
    ][0]
    PaymentForm.base_fields["person"] = forms.ModelChoiceField(
        queryset=persons
    )

    # change queryset for event field (only type CNF and status OPN)
    events = Event.objects.filter(
        activity__activity_type="CNF", status="OPN"
    ).order_by("-date")
    PaymentForm.base_fields["event"] = forms.ModelChoiceField(queryset=events)

    context = {
        "title": _("Create Order"),
        "form": PaymentForm(
            initial={
                "person": current_person,
                "ref_month": timezone.now().date(),
            }
        ),
        "hx_post": reverse("order_add_payment"),
        "hx_target": "#payments",
        "hx_swap": "beforeend",
    }
    return render(request, template_name, context)


@require_http_methods(["DELETE"])
def order_del_payment(request, pay_id):
    template_name = "treasury/order/elements/payments.html"
    for payment in request.session["order"]["payments"]:
        if payment["id"] == pay_id:
            request.session["order"]["total_payments"] -= float(
                payment["value"]
            )
            request.session["order"]["missing"] -= float(payment["value"])
            request.session["order"]["payments"].remove(payment)
            break
    request.session.modified = True

    return render(request, template_name)


def order_add_payform(request):
    template_name = "treasury/order/elements/payform_add.html"
    if request.method == "POST":
        template_name = "treasury/order/elements/payform.html"
        _ids = (
            [int(i["id"]) for i in request.session["order"]["payforms"]]
            if request.session["order"]["payments"]
            else 0
        )
        new = {
            "id": max(_ids) + 1 if _ids else 1,
            "payform_type": {},
            "bank_flag": {},
            "ctrl_number": None,
            "complement": None,
            "value": 0.0,
            "voucher_img": None,
        }

        if request.POST.get("payform_type"):
            pftp = [
                pft
                for pft in PAYFORM_TYPES
                if pft[0] == request.POST.get("payform_type")
            ]
            new["payform_type"] = pftp[0]

        if request.POST.get("bank_flag"):
            bank_flag = BankFlags.objects.get(id=request.POST.get("bank_flag"))
            new["bank_flag"] = {"name": bank_flag.name, "id": bank_flag.id}

        if request.POST.get("ctrl_number"):
            new["ctrl_number"] = request.POST.get("ctrl_number")

        if request.POST.get("complement"):
            new["complement"] = request.POST.get("complement")

        if request.POST.get("value"):
            value = float(request.POST.get("value"))
            new["value"] = value
            request.session["order"]["total_payforms"] += value
            request.session["order"]["missing"] -= value

        request.session["order"]["payforms"].append(new)
        request.session.modified = True

        context = {"object": new}
        return render(request, template_name, context)

    context = {
        "form": FormOfPaymentForm(
            initial={"value": request.session["order"]["missing"]}
        ),
        "title": _("Add Form of Payment"),
        "hx_post": reverse("order_add_payform"),
        "hx_target": "#payforms",
        "hx_swap": "beforeend",
    }
    return render(request, template_name, context)


@require_http_methods(["DELETE"])
def order_del_payform(request, pay_id):
    template_name = "treasury/order/elements/payforms.html"
    for payform in request.session["order"]["payforms"]:
        if payform["id"] == pay_id:
            request.session["order"]["total_payforms"] -= float(
                payform["value"]
            )
            request.session["order"]["missing"] += float(payform["value"])
            request.session["order"]["payforms"].remove(payform)
            break
    request.session.modified = True

    return render(request, template_name)


@require_http_methods(["POST"])
def order_register(request):
    request.session["order"]["description"] = request.POST.get("description")
    request.session["order"]["status"] = request.POST.get("status")
    request.session.modified = True

    # get payer
    payer = Person.objects.get(id=request.session["order"]["person"]["id"])

    # create or update order
    if request.session["order"].get("id"):
        order = Order.objects.get(id=request.session["order"]["id"])
        order.payments.all().delete()
        order.form_of_payments.all().delete()
        order.amount = request.session["order"]["total_payments"]
        order.status = request.session["order"]["status"]
        order.description = request.session["order"]["description"]
        order.save()
    else:
        order = Order.objects.create(
            center=request.user.person.center,
            person=payer,
            amount=request.session["order"]["total_payments"],
            status=request.session["order"]["status"],
            description=request.session["order"]["description"],
        )

    # get payments
    for pay in request.session["order"]["payments"]:
        payment = {
            "paytype": PayTypes.objects.get(id=pay["paytype"]["id"]),
            "person": Person.objects.get(id=pay["person"]["id"]),
            "ref_month": pay["ref_month"]["ref"],
            "event": Event.objects.get(id=pay["event"]["id"])
            if pay["event"]
            else None,
            "value": pay["value"],
            "obs": pay["obs"],
        }
        order.payments.create(**payment)

    # get payforms
    for pf in request.session["order"]["payforms"]:
        payform = {
            "payform_type": pf["payform_type"][0],
            "bank_flag": BankFlags.objects.get(id=pf["bank_flag"]["id"])
            if pf["bank_flag"]
            else None,
            "ctrl_number": pf["ctrl_number"],
            "complement": pf["complement"],
            "value": pf["value"],
        }
        order.form_of_payments.create(**payform)

    return redirect("orders")


@login_required
@permission_required("treasury.view_order")
def order_detail(request, id):
    template_name = "treasury/order/detail.html"
    order = Order.objects.get(id=id)
    _status = [o for o in ORDER_STATUS if o[0] == order.status]
    request.session["order"] = {
        "id": str(order.id),
        "created_on": order.created_on.strftime("%d/%m/%y"),
        "person": {},
        "payments": [],
        "payforms": [],
        "total_payments": 0.0,
        "total_payforms": 0.0,
        "missing": 0.0,
        "status": {"descr": _status[0][1], "cod": _status[0][0]},
        "description": order.description,
        "self_payed": order.self_payed,
    }

    # get person
    request.session["order"]["person"] = {
        "name": order.person.name,
        "id": str(order.person.id),
    }

    # get payments
    for n, pay in enumerate(order.payments.all()):
        _event = {}
        if pay.event:
            _event = {
                "name": "{}... {} ({})".format(
                    pay.event.activity.name[:4],
                    pay.event.center,
                    pay.event.date.strftime("%d/%m/%y"),
                ),
                "id": str(pay.event.id),
            }
        payment = {
            "id": n + 1,
            "paytype": {
                "name": pay.paytype.name,
                "id": pay.paytype.id,
            },
            "person": {
                "name": short_name(pay.person.name),
                "id": str(pay.person.id),
            },
            "ref_month": {
                "repr": pay.ref_month.strftime("%b/%y"),
                "ref": pay.ref_month.strftime("%Y-%m-%d"),
            },
            "event": _event,
            "value": float(pay.value),
            "obs": pay.obs,
        }
        request.session["order"]["payments"].append(payment)
        request.session["order"]["total_payments"] += float(pay.value)

    # get payforms
    for n, pf in enumerate(order.form_of_payments.all()):
        pft = [_pft for _pft in PAYFORM_TYPES if _pft[0] == pf.payform_type]
        payform = {
            "id": n + 1,
            "payform_type": pft[0],
            "bank_flag": {"name": pf.bank_flag.name, "id": pf.bank_flag.id}
            if pf.bank_flag
            else None,
            "ctrl_number": pf.ctrl_number,
            "complement": pf.complement,
            "value": float(pf.value),
            "voucher_img": pf.voucher_img.url if pf.voucher_img else None,
        }
        request.session["order"]["payforms"].append(payform)
        request.session["order"]["total_payforms"] += float(pf.value)

    context = {
        "title": _("View Order"),
        "detail": True,
        "form_update_status": FormUpdateStatus(
            initial={"status": _status[0][0]}
        ),
        "goback": reverse("orders"),
    }
    return render(request, template_name, context)


@login_required
@permission_required("treasury.change_order")
def order_update(request, id):
    context = {
        "title": _("Edit Order"),
        "status": ORDER_STATUS,
    }
    return render(request, "treasury/order/create.html", context)


@login_required
@permission_required("treasury.change_order")
def order_update_status(request, id):
    order = Order.objects.get(id=id)
    order.status = request.POST.get("status")
    order.save()

    return redirect("orders")


@login_required
@permission_required("treasury.delete_order")
def order_delete(request, id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.payments.all().delete()
        order.form_of_payments.all().delete()
        order.delete()
        return redirect("orders")

    context = {
        "object": order,
        "title": _("confirm to delete"),
    }
    return render(request, "treasury/elements/confirm_delete.html", context)
