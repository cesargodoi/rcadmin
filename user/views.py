import datetime
import json

from django.template.loader import render_to_string
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from event.models import Event
from person.models import Historic
from treasury.models import BankFlags, Order, PayTypes
from rcadmin.common import PROFILE_PAYFORM_TYPES, check_center_module

from .forms import (
    UserForm,
    UserFormReadonly,
    ProfileFormUpdate,
    ImageFormUpdate,
    MyPaymentForm,
    MyFormOfPaymentForm,
)

modal_updated_triggers = json.dumps(
    {
        "closeModal": True,
        "showToast": _("The Profile has been updated!"),
    }
)


@login_required
@permission_required("user.view_profile")
def profile_detail(request):
    template_name = "user/profile/detail.html"
    context = {
        "object": request.user,
        "tab": "detail",
    }
    return render(request, template_name, context)


@login_required
@permission_required("user.change_profile")
def updt_profile(request):
    template_name = "user/forms/updt_profile.html"
    if request.method == "POST":
        # updating the user
        user_form = UserFormReadonly(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
        # updating the user.profile
        profile_form = ProfileFormUpdate(
            request.POST, instance=request.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()

            template_name = "user/profile/elements/tab_profile.html"
            context = {"object": request.user, "updated": True}
            return HttpResponse(
                render_to_string(template_name, context, request),
                headers={
                    "HX-Retarget": "#tabProfile",
                    "HX-Trigger": modal_updated_triggers,
                },
            )
    else:
        user_form = UserFormReadonly(instance=request.user)
        profile_form = ProfileFormUpdate(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "title": _("update profile"),
        "object": request.user,
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("user.change_profile")
def updt_image(request):
    if request.method == "POST":
        # updating the user.profile
        image_form = ImageFormUpdate(
            request.POST, request.FILES, instance=request.user.profile
        )
        if image_form.is_valid():
            image_form.save()

            template_name = "user/profile/elements/tab_image.html"
            context = {"object": request.user, "updated": True}
            return HttpResponse(
                render_to_string(template_name, context, request),
                headers={
                    "HX-Retarget": "#tabImage",
                    "HX-Trigger": modal_updated_triggers,
                },
            )
    else:
        image_form = ImageFormUpdate(instance=request.user.profile)

    template_name = "user/forms/updt_image.html"
    context = {
        "title": _("Update image"),
        "image_form": image_form,
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("user.view_profile")
def user_frequencies(request):
    template_name = "user/profile/detail.html"
    frequencies = request.user.person.event_set.all().order_by("-date")
    context = {
        "frequencies": frequencies[:20],
        "count": frequencies.count(),
        "object": request.user,
        "tab": "frequencies",
    }
    return render(request, template_name, context)


@login_required
@permission_required("user.view_profile")
def user_historic(request):
    template_name = "user/profile/detail.html"
    historic = Historic.objects.filter(person=request.user.person).order_by(
        "-date"
    )
    context = {
        "historic": historic[:20],
        "count": len(historic),
        "object": request.user,
        "tab": "historic",
    }
    return render(request, template_name, context)


@login_required
def scan_qrcode_event(request):
    template_name = "user/profile/scan_qrcode_event.html"
    if request.method == "POST":
        event = get_object_or_404(Event, id=request.POST.get("qrcode"))
        event.frequencies.add(request.user.person)
        message = _("You are registered for the event: %s") % (event)
        messages.success(request, message)
        return redirect(reverse("user_frequencies"))

    context = {
        "object": request.user,
    }
    return render(request, template_name, context)


@login_required
def user_payments(request):
    if not check_center_module(request, "treasury"):
        return render(request, "base/module_not_avaiable.html")

    template_name = "user/profile/detail.html"
    if request.session.get("my_order"):
        del request.session["my_order"]
    payments = request.user.person.payment_set.all().order_by("-created_on")

    context = {
        "payments": payments[:20],
        "count": len(payments),
        "object": request.user,
        "tab": "payments",
    }
    return render(request, template_name, context)


@login_required
def user_new_order(request):
    if not check_center_module(request, "treasury"):
        return render(request, "base/module_not_avaiable.html")

    template_name = "user/profile/new_order.html"
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
        "title": _("Create my order"),
        "object": request.user,
        "form": MyFormOfPaymentForm(
            initial={"value": request.session["my_order"]["total_payments"]}
        ),
        "from_user": True,
    }
    return render(request, template_name, context)


def user_how_to_pay(request):
    template_name = "user/profile/elements/how_to_pay.html"
    return render(request, template_name)


@login_required
def user_add_payment(request):
    template_name = "user/profile/elements/payment_add.html"

    if request.method == "POST":
        template_name = "user/profile/elements/payment.html"

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

        context = {"object": new}
        return render(request, template_name, context)

    # change queryset for event field (only type CNF and status OPN)
    events = Event.objects.filter(
        activity__activity_type="CNF", status="OPN"
    ).order_by("-date")
    MyPaymentForm.base_fields["event"] = forms.ModelChoiceField(
        queryset=events
    )

    context = {
        "form": MyPaymentForm(
            initial={
                "paytype": None,
                "person": request.user.person,
                "ref_month": timezone.now().date(),
            }
        ),
        "title": _("Create my order - add payment"),
        "object": request.user,
        "hx_post": reverse("user_add_payment"),
        "hx_target": "#payments",
        "hx_swap": "beforeend",
    }
    return render(request, template_name, context)


@login_required
@require_http_methods(["DELETE"])
def user_del_payment(request, pay_id):
    template_name = "user/profile/elements/payments.html"
    for payment in request.session["my_order"]["payments"]:
        if payment["id"] == pay_id:
            request.session["my_order"]["total_payments"] -= float(
                payment["value"]
            )
            request.session["my_order"]["missing"] -= float(payment["value"])
            request.session["my_order"]["payments"].remove(payment)
            break
    request.session.modified = True

    return render(request, template_name)
