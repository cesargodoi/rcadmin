from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from rcadmin.common import clear_session
from base.searchs import search_center
from django.http.response import Http404
from person.models import Person

from rcadmin.common import get_template_and_pagination
from .forms import CenterForm, SelectNewCenterForm
from .models import Center


@login_required
@permission_required("center.view_center")
def center_home(request):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request, "center/home.html", "center/elements/center_list.html"
    )

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_center(request, Center, _from, _to)
        # add action links
        for item in object_list:
            item.click_link = reverse("center_detail", args=[item.pk])

    if not request.htmx and object_list:
        message = f"{count} records were found in the database"
        messages.success(request, message)

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "init": True if request.GET.get("init") else False,
        "title": _("center home"),
        "nav": "home",
    }
    return render(request, template_name, context)


@login_required
@permission_required("center.view_center")
def center_detail(request, pk):
    center = Center.objects.get(pk=pk)
    users = center.person_set.filter(is_active=True).count()
    goback = (
        reverse("home") if request.GET.get("from") else reverse("center_home")
    )

    context = {
        "object": center,
        "title": _("center detail"),
        "users": users,
        "nav": "detail",
        "goback": goback,
    }
    return render(request, "center/detail.html", context)


@login_required
@permission_required("center.add_center")
def center_create(request):
    if request.method == "POST":
        form = CenterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            message = f"The Center '{request.POST['name']}' has been created!"
            messages.success(request, message)
            return redirect(reverse("center_home") + "?init=on")
        else:
            message = "There are some errors in the form, please correct them."
            messages.warning(request, message)

    context = {
        "form": CenterForm(
            request.POST or None, initial={"made_by": request.user}
        ),
        "form_name": "Center",
        "form_path": "center/forms/center.html",
        "goback": reverse("center_home"),
        "title": _("create center"),
        "to_create": True,
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("center.change_center")
def center_update(request, pk):
    persons = [psn.id for psn in Person.objects.filter(center=pk)]
    if request.user.person.pk in persons or request.user.is_superuser:
        center = Center.objects.get(pk=pk)

        if request.method == "POST":
            form = CenterForm(request.POST, request.FILES, instance=center)
            if form.is_valid():
                form.save()
                message = (
                    f"The Center '{request.POST['name']}' has been updated!"
                )
                messages.success(request, message)
                return redirect("center_detail", pk=pk)
    else:
        raise Http404

    context = {
        "form": CenterForm(instance=center),
        "form_name": "Center",
        "form_path": "center/forms/center.html",
        "goback": reverse("center_detail", args=[pk]),
        "title": _("update center"),
        "id": pk,
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("center.delete_center")
def center_delete(request, pk):
    center = Center.objects.get(pk=pk)
    if request.method == "POST":
        if request.POST.get("conf_center"):
            _center = Center.objects.get(pk=request.POST.get("conf_center"))
            persons = center.person_set.all()
            for person in persons:
                person.center = _center
                person.save()
        center.is_active = False
        center.save()
        return redirect(reverse("center_home") + "?init=on")

    context = {
        "object": center,
        "new_center": SelectNewCenterForm() if center.person_set.all() else "",
        "title": _("confirm to delete"),
    }
    return render(request, "center/confirm_delete.html", context)


@login_required
@permission_required("center.add_center")
def center_reinsert(request, pk):
    center = Center.objects.get(pk=pk)
    if request.method == "POST":
        center.is_active = True
        center.save()
        return redirect(reverse("center_home") + "?init=on")

    context = {
        "object": center,
        "title": _("confirm to reinsert"),
    }
    return render(request, "center/confirm_reinsert.html", context)
