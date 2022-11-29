from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from rcadmin.common import SEEKER_STATUS
from ..forms import HistoricForm
from ..models import Seeker, HistoricOfSeeker


@login_required
@permission_required("publicwork.add_historicofseeker")
def create_historic(request, pk):
    seeker = Seeker.objects.get(pk=pk)

    if request.method == "POST":
        form = HistoricForm(request.POST)
        if form.is_valid():
            form.save()
            if request.POST.get("occurrence") != "OBS":
                adjust_seeker_side(
                    seeker,
                    request.POST.get("occurrence"),
                    request.POST.get("date"),
                )

            messages.success(request, "The Historic has been created!")
        return redirect("seeker_historic", pk=pk)

    template_name = "publicwork/seeker/forms/historic.html"
    context = {
        "form": HistoricForm(
            initial={
                "seeker": seeker,
                "date": timezone.now(),
                "occurrence": "OBS",
                "made_by": request.user,
            }
        ),
        "title": _("Create historic"),
        "callback_link": reverse("create_historic", args=[pk]),
        "target": "historicList",
        "swap": "innerHTML",
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.change_historicofseeker")
def update_historic(request, seek_pk, hist_pk):
    seeker = Seeker.objects.get(pk=seek_pk)
    historic = HistoricOfSeeker.objects.get(pk=hist_pk)

    if request.method == "POST":
        form = HistoricForm(request.POST, instance=historic)
        if form.is_valid():
            form.save()
            if request.POST.get("occurrence") != "OBS":
                adjust_seeker_side(
                    seeker,
                    request.POST.get("occurrence"),
                    request.POST.get("date"),
                )

        historic.update_link = reverse(
            "update_historic", args=[seek_pk, hist_pk]
        )
        historic.delete_link = reverse(
            "delete_historic", args=[seek_pk, hist_pk]
        )

        template_name = "publicwork/seeker/elements/hx/historic_updated.html"
        context = {"obj": historic, "pos": request.GET.get("pos")}
        return render(request, template_name, context)

    template_name = "publicwork/seeker/forms/historic.html"
    context = {
        "form": HistoricForm(instance=historic),
        "title": _("Update historic"),
        "callback_link": reverse("update_historic", args=[seek_pk, hist_pk]),
        "target": f"HST{hist_pk}",
        "swap": "innerHTML",
        "pos": request.GET.get("pos"),
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.delete_historicofseeker")
def delete_historic(request, seek_pk, hist_pk):
    historic = HistoricOfSeeker.objects.get(pk=hist_pk)
    if request.method == "POST":
        occur = historic.occurrence
        historic.delete()
        if occur not in ("OBS", "NEW"):
            adjust_seeker_side(historic.seeker, reverse=True)
        return redirect("seeker_historic", pk=seek_pk)

    template_name = "publicwork/seeker/confirm/delete.html"
    context = {
        "object": "{} ⛔️ {}".format(
            historic.seeker.name,
            dict(SEEKER_STATUS)[historic.occurrence].upper(),
        ),
        "callback": reverse("delete_historic", args=[seek_pk, hist_pk]),
    }
    return render(request, template_name, context)


# handlers
def adjust_seeker_side(seeker, occur=None, dt=None, reverse=False):
    if reverse:
        old_historic = HistoricOfSeeker.objects.filter(seeker=seeker).last()
        seeker.status = old_historic.occurrence
        seeker.status_date = old_historic.date
        seeker.save()
    else:
        date = datetime.strptime(dt, "%Y-%m-%d").date()
        if not seeker.status_date or date >= seeker.status_date:
            seeker.status = occur
            seeker.status_date = date
            if occur == "RST":
                seeker.is_active = False
            seeker.save()
