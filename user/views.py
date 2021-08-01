import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from event.models import Event
from person.models import Historic
from treasury.models import BankFlags, Order, PayTypes
from schooladmin.common import PROFILE_PAYFORM_TYPES

from .forms import MyFormOfPaymentForm, MyPaymentForm, ProfileForm, UserForm


@login_required
@permission_required("user.view_profile")
def profile_detail(request):
    context = {"object": request.user, "tab": "detail"}
    return render(request, "user/profile_detail.html", context)


@login_required
@permission_required("user.change_profile")
def profile_update(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()
            message = "My Profile has been updated!"
            messages.success(request, message)

        return redirect(reverse("profile_detail"))

    context = {
        "user_form": UserForm(instance=request.user),
        "profile_form": ProfileForm(instance=request.user.profile),
        "title": "update profile",
        "object": request.user,
    }

    return render(request, "user/profile_form.html", context)


@login_required
@permission_required("user.view_profile")
def user_frequencies(request):
    frequencies = request.user.person.event_set.all().order_by("-date")
    context = {
        "frequencies": frequencies[:20],
        "count": frequencies.count(),
        "object": request.user,
        "tab": "frequencies",
    }
    return render(request, "user/profile_detail.html", context)


@login_required
@permission_required("user.view_profile")
def user_historic(request):
    historic = Historic.objects.filter(person=request.user.person).order_by(
        "-date"
    )
    context = {
        "historic": historic[:20],
        "count": historic.count(),
        "object": request.user,
        "tab": "historic",
    }
    return render(request, "user/profile_detail.html", context)


@login_required
def scan_qrcode_event(request):
    if request.method == "POST":
        event = get_object_or_404(Event, id=request.POST.get("id"))
        event.frequencies.add(request.user.person)
        message = f"You are registered for the event: {event}"
        messages.success(request, message)
        return redirect(reverse("user_frequencies"))

    context = {
        "object": request.user,
    }
    return render(request, "user/scan_qrcode_event.html", context)


@login_required
def user_payments(request):
    if request.session.get("my_order"):
        del request.session["my_order"]
    payments = request.user.person.payment_set.all().order_by("-created_on")

    context = {
        "payments": payments[:20],
        "object": request.user,
        "tab": "payments",
    }
    return render(request, "user/profile_detail.html", context)


@login_required
def user_new_order(request):
    if not request.session.get("my_order"):
        request.session["my_order"] = {
            "person": {
                "name": request.user.person.name,
                "id": str(request.user.person.id),
            },
            "payments": [],
            "total_payments": 0.0,
            "total_payform": 0.0,
            "missing": 0.0,
            "description": "",
        }

    if request.method == "POST":
        # generate order
        new_order = {
            "center": request.user.person.center,
            "person": request.user.person,
            "amount": request.session["my_order"]["total_payments"],
            "status": "PND",
            "description": request.POST.get("description"),
            "self_payed": True,
        }
        order = Order.objects.create(**new_order)
        # get payments
        for pay in request.session["my_order"]["payments"]:
            payment = {
                "paytype": PayTypes.objects.get(id=pay["paytype"]["id"]),
                "person": request.user.person,
                "ref_month": pay["ref_month"]["ref"],
                "event": Event.objects.get(id=pay["event"]["id"])
                if pay["event"]
                else None,
                "value": pay["value"],
                "obs": pay["obs"],
            }
            order.payments.create(**payment)
        # get payform
        payform_type = [
            pft
            for pft in PROFILE_PAYFORM_TYPES
            if pft[0] == request.POST.get("type")
        ]
        payform = {
            "payform_type": payform_type[0][0],
            "bank_flag": BankFlags.objects.get(id=request.POST["bank_flag"])
            if request.POST.get("bank_flag")
            else None,
            "ctrl_number": request.POST.get("ctrl_number"),
            "complement": request.POST.get("complement"),
            "value": request.POST.get("value"),
            "voucher_img": request.FILES["voucher_img"]
            if request.FILES.get("voucher_img")
            else None,
        }
        order.form_of_payments.create(**payform)

        return redirect("user_payments")

    context = {
        "title": "Create my order",
        "object": request.user,
        "form": MyFormOfPaymentForm(
            initial={"value": request.session["my_order"]["total_payments"]}
        ),
        "from_user": True,
    }
    return render(request, "user/profile_new_order.html", context)


@login_required
def add_payment(request):
    if request.method == "POST":
        _ids = (
            [int(i["id"]) for i in request.session["my_order"]["payments"]]
            if request.session["my_order"]["payments"]
            else 0
        )
        new = {
            "id": max(_ids) + 1 if _ids else 1,
            "paytype": {},
            "person": {
                "name": request.user.person.short_name,
                "id": str(request.user.person.id),
            },
            "ref_month": {},
            "event": {},
            "value": 0.0,
            "obs": "",
        }

        if request.POST.get("paytype"):
            paytype = PayTypes.objects.get(id=request.POST.get("paytype"))
            new["paytype"] = {"name": paytype.name, "id": paytype.id}

        if request.POST.get("ref_month"):
            ref = request.POST.get("ref_month")
            _repr = datetime.datetime.strptime(ref, "%Y-%m-%d").date()
            new["ref_month"] = {"repr": _repr.strftime("%b/%y"), "ref": ref}

        if request.POST.get("event"):
            event = get_object_or_404(Event, id=request.POST.get("event"))
            _event = "{}... {} ({})".format(
                event.activity.name[:4],
                event.center,
                event.date.strftime("%d/%m/%y"),
            )
            new["event"] = {"name": _event, "id": str(event.id)}

        if request.POST.get("value"):
            value = float(request.POST.get("value"))
            new["value"] = value
            request.session["my_order"]["total_payments"] += value
            request.session["my_order"]["missing"] += value

        if request.POST.get("obs"):
            new["obs"] = request.POST.get("obs")[:50]

        request.session["my_order"]["payments"].append(new)
        request.session.modified = True
        return redirect("user_new_order")

    context = {
        "form": MyPaymentForm(
            initial={
                "paytype": PayTypes.objects.first()
                if len(PayTypes.objects.all()) > 0
                else None,
                "person": request.user.person,
                "ref_month": timezone.now().date(),
            }
        ),
        "title": "Create my order - add payment",
        "object": request.user,
    }
    return render(request, "user/profile_add_payment.html", context)


@login_required
def del_payment(request, pay_id):
    if request.method == "POST":
        for payment in request.session["my_order"]["payments"]:
            if payment["id"] == pay_id:
                request.session["my_order"]["total_payments"] -= float(
                    payment["value"]
                )
                request.session["my_order"]["missing"] -= float(
                    payment["value"]
                )
                request.session["my_order"]["payments"].remove(payment)
                break
        request.session.modified = True
        return redirect("user_new_order")

    context = {"title": "confirm delete"}
    return render(request, "user/elements/confirm_del.html", context)
