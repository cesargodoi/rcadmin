from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from person.models import Person

from rcadmin.common import get_template_and_pagination
from ..forms import FrequenciesAddForm
from ..models import Event


@require_http_methods(["GET", "DELETE"])
@login_required
@permission_required(["event.change_event", "person.change_person"])
def frequency_delete(request, pk, person_id):
    event = Event.objects.get(pk=pk)
    person = event.frequencies.get(id=person_id)

    if request.method == "DELETE":
        event.frequencies.remove(person)

        LIMIT, template_name, _from, _to, page = get_template_and_pagination(
            request, "event/detail.html", "event/elements/frequency_list.html"
        )

        _object_list = event.frequency_set.all().order_by("person__name_sa")
        count = len(_object_list)
        object_list = _object_list[_from:_to]
        # add action links
        for item in object_list:
            item.del_link = reverse(
                "frequency_delete", args=[pk, item.person.pk]
            )

        context = {
            "LIMIT": LIMIT,
            "page": page,
            "counter": (page - 1) * LIMIT,
            "object_list": object_list,
            "count": count,
        }
        return render(request, template_name, context)

    template_name = "event/confirm/delete.html"
    context = {
        "allowed": True,
        "object": f"{person.name} ⛔️ {event}",
        "del_link": reverse("frequency_delete", args=[pk, person_id]),
    }
    return render(request, template_name, context)


@login_required
@permission_required(["event.change_event", "person.change_person"])
def frequencies_add(request, pk):
    object = Event.objects.get(pk=pk)
    regs_on_event = [fr.person.reg for fr in object.frequency_set.all()]
    regs, unknown = [], []

    if request.method == "POST":
        from_request = set(
            [
                reg
                for reg in request.POST.get("frequencies")
                .replace(" ", "")
                .split(",")
                if reg
            ]
        )

        for reg in from_request:
            if reg not in regs_on_event:
                try:
                    person = Person.objects.get(reg=reg)
                    object.frequency_set.create(
                        person=person,
                        event=object,
                        aspect=person.aspect,
                    )
                    regs.append(reg)
                except Exception:
                    unknown.append(reg)
        if len(regs) > 0:
            message = f"{len(regs)} persons were launched at this Event. "
            messages.success(request, message)
        if not unknown:
            return redirect("event_detail", pk=pk)

    template_name = "event/elements/frequencies-add.html"
    context = {
        "object": object,
        "form": FrequenciesAddForm(),
        "title": _("insert frequencies"),
        "unknown": unknown if len(unknown) > 0 else None,
    }
    return render(request, template_name, context)
