from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import paginator

from ..forms import PaymentForm
from ..models import Payment


@login_required
@permission_required("treasury.view_payment")
def payments(request):
    queryset = Payment.objects.all()
    object_list = paginator(queryset, page=request.GET.get("page"))

    context = {
        "object_list": object_list,
        "title": _("Payments"),
    }
    return render(request, "treasury/payment/home.html", context)


@login_required
@permission_required("treasury.add_payment")
def payment_create(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            message = _("The Payment has been created!")
            messages.success(request, message)
            return redirect("payments")

    context = {
        "form": PaymentForm(),
        "form_name": _("Payment"),
        "form_path": "treasury/elements/generic_form.html",
        "goback": reverse("payments"),
        "to_create": True,
        "title": _("Create Payment"),
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("treasury.change_payment")
def payment_update(request, pk):
    payment = Payment.objects.get(pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            message = _("The Payment has been updated!")
            messages.success(request, message)
            return redirect("payments")

    context = {
        "form": PaymentForm(instance=payment),
        "form_name": _("Payment"),
        "form_path": "treasury/elements/generic_form.html",
        "goback": reverse("payments"),
        "title": _("Update Payment"),
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("treasury.delete_payment")
def payment_delete(request, pk):
    payment = Payment.objects.get(pk=pk)
    if request.method == "POST":
        if not payment.order_set.all():
            payment.delete()
            message = _("The Payment has been deleted!")
            messages.success(request, message)
        return redirect("payments")

    context = {
        "object": payment,
        "title": _("confirm to delete"),
    }
    return render(request, "treasury/elements/confirm_delete.html", context)
