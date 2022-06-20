from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.http.response import Http404
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import (
    LECTURE_TYPES,
    clear_session,
    get_template_and_pagination,
)
from base.searchs import search_lecture


from ..forms import LectureForm
from ..models import Lecture


@login_required
@permission_required("publicwork.view_lecture")
def lecture_home(request):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/lecture/home.html",
        "publicwork/lecture/elements/lecture_list.html",
    )

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_lecture(request, Lecture, _from, _to)
        # add action links
        for item in object_list:
            item.click_link = reverse("lecture_detail", args=[item.pk])

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
        "title": _("lecture home"),
        "type_list": LECTURE_TYPES,
        "nav": "lc_home",
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.view_lecture")
def lecture_detail(request, pk):
    lect_object = Lecture.objects.get(pk=pk)

    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request,
        "publicwork/lecture/detail.html",
        "publicwork/listener/elements/listener_list.html",
    )

    _object_list = lect_object.listener_set.all().order_by("seeker__name_sa")

    count = len(_object_list)
    object_list = _object_list[_from:_to]

    # add action links
    for item in object_list:
        item.click_link = reverse("update_listener", args=[pk, item.pk])
        item.del_link = reverse("remove_listener", args=[pk, item.pk])

    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "object": lect_object,
        "title": _("lecture detail"),
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.add_lecture")
def lecture_create(request):
    if request.method == "POST":
        form = LectureForm(request.POST)
        if form.is_valid():
            form.save()
            message = (
                f"The lecture '{request.POST['theme']}' has been created!"
            )
            messages.success(request, message)
            return redirect(reverse("lecture_home"))

    lecture_form = LectureForm(
        initial={
            "made_by": request.user,
            "center": request.user.person.center,
            "date": datetime.now().date,
        }
    )

    template_name = "publicwork/lecture/forms/lecture.html"
    context = {
        "form": lecture_form,
        "callback": reverse("lecture_create"),
        "title": _("Create lecture"),
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.change_lecture")
def lecture_update(request, pk):
    lect_object = Lecture.objects.get(pk=pk)
    if lect_object.center != request.user.person.center:
        raise Http404

    if request.method == "POST":
        form = LectureForm(request.POST, instance=lect_object)
        if form.is_valid():
            form.save()
            # message = (
            #     f"The lecture '{request.POST['theme']}' has been updated!"
            # )
            # messages.success(request, message)
            template_name = "publicwork/lecture/header.html"
            context = {"object": lect_object}
            return render(request, template_name, context)

    lecture_form = LectureForm(
        instance=lect_object,
        initial={"made_by": request.user},
    )

    template_name = "publicwork/lecture/forms/lecture.html"
    context = {
        "form": lecture_form,
        "callback": reverse("lecture_update", args=[pk]),
        "target": "header",
        "swap": "innerHTML",
        "title": _("Update lecture"),
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("publicwork.delete_lecture")
def lecture_delete(request, pk):
    lect_object = Lecture.objects.get(pk=pk)
    if lect_object.center != request.user.person.center:
        raise Http404

    if request.method == "POST":
        lect_object.delete()
        message = _("The lecture has been deleted!")
        messages.success(request, message)
        return redirect("lecture_home")

    template_name = "publicwork/confirm/delete.html"
    context = {
        "object": lect_object,
        "del_link": reverse("lecture_delete", args=[pk]),
    }
    return render(request, template_name, context)
