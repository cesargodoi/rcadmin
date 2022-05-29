from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from person.models import Person

from ..forms import FrequenciesAddForm
from ..models import Event


@login_required
@permission_required(["event.change_event", "person.change_person"])
def frequency_delete(request, pk, person_id):
    event = Event.objects.get(pk=pk)
    person = event.frequencies.get(id=person_id)
    object = f"Remove: {person.name} from: {event}"
    if request.method == "POST":
        event.frequencies.remove(person)
        message = _("The Frequency has been deleted!")
        messages.success(request, message)
        return redirect("event_detail", pk=pk)

    context = {
        "object": object,
        "title": _("confirm to delete"),
    }
    return render(request, "base/confirm_delete.html", context)


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

    context = {
        "object": object,
        "form": FrequenciesAddForm(),
        "title": _("insert frequencies"),
        "unknown": unknown if len(unknown) > 0 else None,
    }
    return render(request, "event/frequencies-add.html", context)
