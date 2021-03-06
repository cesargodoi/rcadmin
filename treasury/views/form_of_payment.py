from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import paginator

from ..forms import FormOfPaymentForm
from ..models import FormOfPayment


@login_required
@permission_required("treasury.view_formofpayment")
def forms_of_payments(request):
    queryset = FormOfPayment.objects.all()
    object_list = paginator(queryset, page=request.GET.get("page"))

    context = {
        "object_list": object_list,
        "title": _("Forms of Payables"),
    }
    return render(request, "treasury/form_of_payment/home.html", context)


@login_required
@permission_required("treasury.add_formofpayment")
def form_of_payment_create(request):
    if request.method == "POST":
        form = FormOfPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            message = _("The Form of Payment has been created!")
            messages.success(request, message)
            return redirect("forms_of_payments")

    context = {
        "form": FormOfPaymentForm(),
        "form_name": "Form of Payment",
        "form_path": "treasury/elements/generic_form.html",
        "goback": reverse("forms_of_payments"),
        "to_create": True,
        "title": _("Create Form of Payment"),
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("treasury.change_formofpayment")
def form_of_payment_update(request, pk):
    form_of_payment = FormOfPayment.objects.get(pk=pk)
    if request.method == "POST":
        form = FormOfPaymentForm(request.POST, instance=form_of_payment)
        if form.is_valid():
            form.save()
            message = _("The Form of Payment has been updated!")
            messages.success(request, message)
            return redirect("forms_of_payments")

    context = {
        "form": FormOfPaymentForm(instance=form_of_payment),
        "form_name": "Form of Payment",
        "form_path": "treasury/elements/generic_form.html",
        "goback": reverse("forms_of_payments"),
        "title": _("Update Form of Payment"),
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("treasury.delete_formofpayment")
def form_of_payment_delete(request, pk):
    form_of_payment = FormOfPayment.objects.get(pk=pk)
    if request.method == "POST":
        if not form_of_payment.order_set.all():
            form_of_payment.delete()
            message = _("The Form of Payment has been deleted!")
            messages.success(request, message)
        return redirect("forms_of_payments")

    context = {
        "object": form_of_payment,
        "title": _("confirm to delete"),
    }
    return render(request, "treasury/elements/confirm_delete.html", context)
