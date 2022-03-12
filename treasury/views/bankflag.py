from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import paginator

from ..forms import BankFlagForm
from ..models import BankFlags


@login_required
@permission_required("treasury.view_bankflags")
def bankflags(request):
    queryset = BankFlags.objects.all()
    object_list = paginator(queryset, page=request.GET.get("page"))

    context = {
        "object_list": object_list,
        "title": _("Banks or Flags"),
    }
    return render(request, "treasury/bankflag/home.html", context)


@login_required
@permission_required("treasury.add_bankflags")
def bankflag_create(request):
    if request.method == "POST":
        form = BankFlagForm(request.POST)
        if form.is_valid():
            form.save()
            message = _("The Bank or Flag has been created!")
            messages.success(request, message)
            return redirect("bankflags")

    context = {
        "form": BankFlagForm(),
        "form_name": "Bank or Flag",
        "form_path": "treasury/elements/generic_form.html",
        "goback": reverse("bankflags"),
        "to_create": True,
        "title": _("Create Bank or flag"),
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("treasury.change_bankflags")
def bankflag_update(request, pk):
    bank_flag = BankFlags.objects.get(pk=pk)
    if request.method == "POST":
        form = BankFlagForm(request.POST, instance=bank_flag)
        if form.is_valid():
            form.save()
            message = _("The Bank or Flag has been updated!")
            messages.success(request, message)
            return redirect("bankflags")

    context = {
        "form": BankFlagForm(instance=bank_flag),
        "form_name": "Bank or flag",
        "form_path": "treasury/elements/generic_form.html",
        "goback": reverse("bankflags"),
        "title": _("Update Bank or Flag"),
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("treasury.delete_bankflags")
def bankflag_delete(request, pk):
    bank_flag = BankFlags.objects.get(pk=pk)
    if request.method == "POST":
        if bank_flag.formofpayment_set.all():
            bank_flag.is_active = False
            bank_flag.save()
            message = _("The Bank or Flag has been inactivated!")
        else:
            bank_flag.delete()
            message = _("The Bank or Flag has been deleted!")
        messages.success(request, message)
        return redirect("bankflags")

    context = {
        "object": bank_flag,
        "title": _("confirm to delete"),
    }
    return render(request, "base/confirm_delete.html", context)
