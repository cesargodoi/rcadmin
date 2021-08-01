from datetime import datetime

from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from event.models import Event
from person.models import Person
from schooladmin.common import (
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
        "title": "Orders",
        "nav": "order",
    }
    return render(request, "treasury/orders.html", context)


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
        "title": "Create Order",
        "status": ORDER_STATUS,
    }
    return render(request, "treasury/order_create.html", context)


def order_search_person(request):
    if request.is_ajax():
        term = request.GET.get("term")
        persons = Person.objects.filter(
            name__icontains=term, center=request.user.person.center
        )[:20]
        results = [person.name for person in persons]
        return JsonResponse(results, safe=False)

    return render(request, "treasury/order_create.html")


def order_add_payment(request):
    if request.method == "POST":
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
        return redirect("order_create")

    persons = Person.objects.filter(center=request.user.person.center)
    person = [
        p
        for p in persons
        if p.name == request.session["order"]["person"]["name"]
    ]
    PaymentForm.base_fields["person"] = forms.ModelChoiceField(
        queryset=persons
    )

    context = {
        "form": PaymentForm(
            initial={"person": person[0], "ref_month": timezone.now().date()}
        ),
        "title": "Create Order",
    }
    return render(request, "treasury/order_add_payment.html", context)


def order_del_payment(request, pay_id):
    if request.method == "POST":
        for payment in request.session["order"]["payments"]:
            if payment["id"] == pay_id:
                request.session["order"]["total_payments"] -= float(
                    payment["value"]
                )
                request.session["order"]["missing"] -= float(payment["value"])
                request.session["order"]["payments"].remove(payment)
                break
        request.session.modified = True
        return redirect("order_create")

    context = {"title": "confirm delete"}
    return render(request, "treasury/confirm_del.html", context)


def order_add_payform(request):
    if request.method == "POST":
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
        return redirect("order_create")

    context = {
        "form": FormOfPaymentForm(
            initial={"value": request.session["order"]["missing"]}
        ),
        "title": "Add Form of Payment",
    }
    return render(request, "treasury/order_add_payform.html", context)


def order_del_payform(request, pay_id):
    if request.method == "POST":
        for payform in request.session["order"]["payforms"]:
            if payform["id"] == pay_id:
                request.session["order"]["total_payforms"] -= float(
                    payform["value"]
                )
                request.session["order"]["missing"] += float(payform["value"])
                request.session["order"]["payforms"].remove(payform)
                break
        request.session.modified = True
        return redirect("order_create")

    context = {"title": "confirm delete"}
    return render(request, "treasury/confirm_del.html", context)


def order_register(request):
    if request.method == "POST":
        # get payer
        payer = Person.objects.get(id=request.session["order"]["person"]["id"])

        # create or update order
        if request.session["order"].get("id"):
            order = get_object_or_404(Order, id=request.session["order"]["id"])
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

    request.session["order"]["description"] = request.GET.get("description")
    request.session["order"]["status"] = request.GET.get("status")
    request.session.modified = True

    context = {"title": "confirm register"}
    return render(request, "treasury/confirm_register.html", context)


@login_required
@permission_required("treasury.view_order")
def order_detail(request, id):
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
        "title": "View Order",
        "detail": True,
        "form_update_status": FormUpdateStatus(
            initial={"status": _status[0][0]}
        ),
    }
    return render(request, "treasury/order_detail.html", context)


@login_required
@permission_required("treasury.change_order")
def order_update(request, id):
    context = {
        "title": "Edit Order",
        "status": ORDER_STATUS,
    }
    return render(request, "treasury/order_create.html", context)


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

    context = {"object": order, "title": "confirm to delete"}
    return render(request, "treasury/confirm_delete.html", context)
