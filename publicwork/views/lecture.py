from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.http.response import Http404
from django.urls import reverse
from schooladmin.common import paginator, LECTURE_TYPES, clear_session
from base.searchs import search_lecture


from ..forms import LectureForm
from ..models import Lecture

###############################################################################
@login_required
@permission_required("publicwork.view_lecture")
def lecture_home(request):
    object_list = None
    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset, page = search_lecture(request, Lecture)
        object_list = paginator(queryset, page=page)
        # add action links
        for item in object_list:
            item.click_link = reverse("lecture_detail", args=[item.pk])

    context = {
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "title": "lecture home",
        "type_list": LECTURE_TYPES,
        "nav": "lc_home",
    }
    return render(request, "publicwork/lecture_home.html", context)


@login_required
@permission_required("publicwork.view_lecture")
def lecture_detail(request, pk):
    lect_object = Lecture.objects.get(pk=pk)
    queryset = lect_object.listener_set.all().order_by("seeker__name_sa")

    object_list = paginator(queryset, 25, page=request.GET.get("page"))
    # add action links
    for item in object_list:
        item.click_link = reverse("update_listener", args=[pk, item.pk])
        item.del_link = reverse("remove_listener", args=[pk, item.pk])

    context = {
        "object": lect_object,
        "object_list": object_list,
        "title": "lecture detail",
    }
    return render(request, "publicwork/lecture_detail.html", context)


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
            return redirect(reverse("lecture_home") + "?init=on")

    lecture_form = LectureForm(
        initial={
            "made_by": request.user,
            "center": request.user.person.center,
        }
    )

    context = {
        "form": lecture_form,
        "form_name": "Lecture",
        "form_path": "publicwork/forms/lecture.html",
        "goback": reverse("lecture_home"),
        "title": "create lecture",
        "to_create": True,
    }
    return render(request, "base/form.html", context)


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
            message = (
                f"The lecture '{request.POST['theme']}' has been updated!"
            )
            messages.success(request, message)
            return redirect("lecture_detail", pk=pk)

    lecture_form = LectureForm(
        instance=lect_object,
        initial={"made_by": request.user},
    )

    context = {
        "form": lecture_form,
        "form_name": "Lecture",
        "form_path": "publicwork/forms/lecture.html",
        "goback": reverse("lecture_detail", args=[pk]),
        "title": "update lecture",
        "pk": pk,
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("publicwork.delete_lecture")
def lecture_delete(request, pk):
    lect_object = Lecture.objects.get(pk=pk)
    if lect_object.center != request.user.person.center:
        raise Http404
    if request.method == "POST":
        lect_object.delete()
        message = "The lecture has been deleted!"
        messages.success(request, message)
        return redirect(reverse("lecture_home") + "?init=on")

    context = {
        "object": lect_object,
        "title": "confirm to delete",
    }
    return render(request, "base/confirm_delete.html", context)
