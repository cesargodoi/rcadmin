from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import paginator

from ..forms import PayTypeForm
from ..models import PayTypes


@login_required
@permission_required("treasury.view_paytypes")
def paytypes(request):
    queryset = PayTypes.objects.all()
    object_list = paginator(queryset, page=request.GET.get("page"))

    context = {
        "object_list": object_list,
        "title": "Types of payment",
    }
    return render(request, "treasury/paytype/home.html", context)


@login_required
@permission_required("treasury.add_paytypes")
def paytype_create(request):
    if request.method == "POST":
        form = PayTypeForm(request.POST)
        if form.is_valid():
            form.save()
            message = _("The PayType has been created!")
            messages.success(request, message)
            return redirect("paytypes")

    context = {
        "form": PayTypeForm(),
        "form_name": "Type of payment",
        "form_path": "treasury/elements/generic_form.html",
        "goback": reverse("paytypes"),
        "to_create": True,
        "title": _("Create type of payment"),
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("treasury.change_paytypes")
def paytype_update(request, pk):
    pay_types = PayTypes.objects.get(pk=pk)
    if request.method == "POST":
        form = PayTypeForm(request.POST, instance=pay_types)
        if form.is_valid():
            form.save()
            message = _("The types of payment has been updated!")
            messages.success(request, message)
            return redirect("paytypes")

    context = {
        "form": PayTypeForm(instance=pay_types),
        "form_name": "Type of payment",
        "form_path": "treasury/elements/generic_form.html",
        "goback": reverse("paytypes"),
        "title": _("Update type of payment"),
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("treasury.delete_paytypes")
def paytype_delete(request, pk):
    pay_types = PayTypes.objects.get(pk=pk)
    if request.method == "POST":
        if pay_types.payment_set.all():
            pay_types.is_active = False
            pay_types.save()
            message = _("The types of payment has been inactivated!")
        else:
            pay_types.delete()
            message = _("The types of payment has been deleted!")
        messages.success(request, message)
        return redirect("paytypes")

    context = {
        "object": pay_types,
        "title": _("confirm to delete"),
    }
    return render(request, "base/confirm_delete.html", context)
