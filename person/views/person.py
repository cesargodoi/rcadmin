import json

from datetime import date

from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext as _

from rcadmin.common import (
    ASPECTS,
    STATUS,
    clear_session,
    get_template_and_pagination,
)
from user.models import User
from base.searchs import search_person

from ..forms import (
    PersonForm,
    ProfileForm,
    UserForm,
    ProfileFormUpdate,
    PupilFormUpdate,
    ImageFormUpdate,
)
from ..models import Historic, Person


modal_updated_triggers = json.dumps(
    {
        "closeModal": True,
        "showToast": _("The Person has been updated!"),
    }
)


@login_required
@permission_required("person.view_person")
def person_home(request):
    LIMIT, template_name, _from, _to, page = get_template_and_pagination(
        request, "person/home.html", "person/elements/person_list.html"
    )

    if request.GET.get("init"):
        object_list, count = None, None
        clear_session(request, ["search"])
    else:
        object_list, count = search_person(request, Person, _from, _to)
        # add action links
        for item in object_list:
            item.click_link = reverse("person_detail", args=[item.id])
            item.local = "{} ({}-{})".format(
                item.user.profile.city,
                item.user.profile.state,
                item.user.profile.country,
            )

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
        "aspect_list": ASPECTS,
        "status_list": STATUS,
        "title": _("person home"),
        "nav": "home",
        "flag": "person",
    }
    return render(request, template_name, context)


@login_required
@permission_required("person.view_person")
def person_detail(request, id):
    if not belongs_center(request, id):
        raise Http404

    person = Person.objects.get(id=id)

    context = {
        "object": person,
        "title": _("person detail"),
        "age": (date.today() - person.birth).days // 365,
        "nav": "detail",
        "tab": request.GET.get("tab") or "info",
        "date": timezone.now().date(),
    }
    return render(request, "person/detail.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def person_create(request):
    if request.method == "POST":
        try:
            # creating a new user
            new_user = User.objects.create_user(email=request.POST["email"])
            # add user in "user" group
            new_user.groups.add(Group.objects.get(name="user"))
            # updating the user.profile
            profile_form = ProfileForm(request.POST, instance=new_user.profile)
            if profile_form.is_valid():
                profile_form.save()
            # updating the user.person
            person_form = PersonForm(request.POST, instance=new_user.person)
            if person_form.is_valid():
                person_form.save()
            # the center is the same as the center of the logged in user
            new_user.person.center = request.user.person.center
            new_user.person.save()
            # adjust social_name in profile
            new_user.profile.social_name = new_user.person.short_name
            new_user.profile.save()

            message = f"The Person '{request.POST['name']}' has been created!"
            messages.success(request, message)
            return redirect("person_detail", id=new_user.person.pk)
        except Exception:
            message = "There are some errors in the form, please correct them."
            messages.warning(request, message)

    user_form = UserForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    person_form = PersonForm(
        request.POST or None, initial={"made_by": request.user}
    )

    template_name = "person/forms/create_person.html"
    context = {
        "user_form": user_form,
        "person_form": person_form,
        "profile_form": profile_form,
        "callback_link": reverse("person_create"),
        "title": _("Create person"),
    }
    return render(request, template_name, context)


#  partial updates
@login_required
@permission_required("person.change_person")
def update_profile(request, id):
    if not belongs_center(request, id):
        raise Http404

    person = Person.objects.get(id=id)

    if request.method == "POST":
        # updating the user
        user_form = UserForm(request.POST, instance=person.user)
        if user_form.is_valid():
            user_form.save()

        # updating the user.profile
        profile_form = ProfileFormUpdate(
            request.POST, instance=person.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()

            template_name = "person/elements/tab_profile.html"
            context = {"object": person, "updated": True}
            return HttpResponse(
                render_to_string(template_name, context, request),
                headers={
                    "HX-Retarget": "#tabProfile",
                    "HX-Trigger": modal_updated_triggers,
                },
            )

    else:
        user_form = UserForm(instance=person.user)
        profile_form = ProfileFormUpdate(instance=person.user.profile)

    template_name = "person/forms/update_profile.html"
    context = {
        "title": _("Update profile"),
        "user_form": user_form,
        "profile_form": profile_form,
        "object": person.user,
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("person.change_person")
def update_pupil(request, id):
    if not belongs_center(request, id):
        raise Http404

    person = Person.objects.get(id=id)

    if request.method == "POST":
        # updating the user.person
        form = PupilFormUpdate(request.POST, instance=person)
        if form.is_valid():
            form.save()

            template_name = "person/elements/tab_pupil.html"
            context = {
                "object": person,
                "age": (date.today() - person.birth).days // 365,
                "updated": True,
            }
            return HttpResponse(
                render_to_string(template_name, context, request),
                headers={
                    "HX-Retarget": "#tabPupil",
                    "HX-Trigger": modal_updated_triggers,
                },
            )

    else:
        form = PupilFormUpdate(
            instance=person, initial={"made_by": request.user}
        )

    template_name = "person/forms/update_pupil.html"
    context = {"title": _("Update pupil"), "form": form, "update": True}
    return render(request, template_name, context)


@login_required
@permission_required("person.change_person")
def update_image(request, id):
    if not belongs_center(request, id):
        raise Http404

    person = Person.objects.get(id=id)

    if request.method == "POST":
        # updating the user.profile
        image_form = ImageFormUpdate(
            request.POST, request.FILES, instance=person.user.profile
        )
        if image_form.is_valid():
            image_form.save()

            template_name = "person/elements/tab_image.html"
            context = {"object": person, "updated": True}
            return HttpResponse(
                render_to_string(template_name, context, request),
                headers={
                    "HX-Retarget": "#tabImage",
                    "HX-Trigger": modal_updated_triggers,
                },
            )
    else:
        image_form = ImageFormUpdate(instance=person.user.profile)

    template_name = "person/forms/update_image.html"
    context = {
        "title": _("Update image"),
        "image_form": image_form,
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("person.delete_person")
def person_delete(request, id):
    person = Person.objects.get(id=id)
    if request.method == "POST":
        if person.historic_set.all():
            person.user.is_active = False
            person.user.save()
            person.is_active = False
            person.status = "REM"
            person.save()
            add_historic(person, "REM", request.user)
        else:
            person.user.delete()
        return redirect("person_home")

    template_name = "person/confirm/delete.html"
    context = {
        "object": person,
        "del_link": reverse("person_delete", args=[id]),
    }
    return render(request, template_name, context)


@login_required
@permission_required("person.add_person")
def person_reinsert(request, id):
    person = Person.objects.get(id=id)
    if request.method == "POST":
        person.user.is_active = True
        person.user.save()
        person.is_active = True
        person.status = "ACT"
        person.save()
        add_historic(person, "ACT", request.user)
        return redirect("person_detail", id=id)

    template_name = "person/confirm/reinsert.html"
    context = {
        "object": person,
        "reinsert_link": reverse("person_reinsert", args=[id]),
    }
    return render(request, template_name, context)


# auxiliar functions
def belongs_center(request, id):
    center_persons = [
        person.id
        for person in Person.objects.filter(
            center=request.user.person.center.pk
        )
    ]
    if id not in center_persons and not request.user.is_superuser:
        return False
    return True


def add_historic(person, occurrence, made_by):
    historic = dict(
        person=person,
        occurrence=occurrence,
        date=timezone.now().date(),
        made_by=made_by,
    )
    Historic.objects.create(**historic)
