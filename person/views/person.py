from datetime import date

from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
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
    BasicFormPerson,
    BasicFormProfile,
    OthersFormPerson,
    OthersFormProfile,
    AddressFormProfile,
    ImageFormProfile,
)
from ..models import Historic, Person


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
    persons = [
        psn.id
        for psn in Person.objects.filter(center=request.user.person.center.id)
    ]
    if id in persons or request.user.is_superuser:
        person = Person.objects.get(id=id)
        age = (date.today() - person.birth).days // 365
    else:
        raise Http404

    context = {
        "object": person,
        "title": _("person detail"),
        "age": age,
        "nav": "detail",
        "tab": request.GET.get("tab") or "info",
        "date": timezone.now().date(),
    }
    return render(request, "person/detail.html", context)


@login_required
@permission_required("person.add_person")
def person_create(request):
    if request.method == "POST":
        try:
            # creating a new user
            email = request.POST["email"]
            password = BaseUserManager().make_random_password()
            new_user = User.objects.create_user(
                email=email,
                password=password,
            )
            # add user in "user" group
            user_group = Group.objects.get(name="user")
            new_user.groups.add(user_group)
            # updating the user.profile
            profile_form = ProfileForm(
                request.POST, request.FILES, instance=new_user.profile
            )
            if profile_form.is_valid():
                profile_form.save()
            # updating the user.person
            person_form = PersonForm(request.POST, instance=new_user.person)
            if person_form.is_valid():
                person_form.save()
            # add password in observations
            new_user.person.observations += f"\nfirst password: {password}"
            # the center is the same as the center of the logged in user
            new_user.person.center = request.user.person.center
            new_user.person.save()
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

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "person_form": person_form,
        "form_name": "Person",
        "form_path": "person/forms/person.html",
        "goback": reverse("person_home"),
        "title": _("create person"),
        "to_create": True,
    }
    return render(request, "base/form.html", context)


#  partial updates
@login_required
@permission_required("person.change_person")
def person_update_basic(request, id):
    center_persons = [
        person.id
        for person in Person.objects.filter(
            center=request.user.person.center.pk
        )
    ]
    if id not in center_persons and not request.user.is_superuser:
        raise Http404

    person = Person.objects.get(id=id)

    if request.method == "POST":
        # updating the user
        user_form = UserForm(request.POST, instance=person.user)
        if user_form.is_valid():
            user_form.save()

        # updating the user.profile
        profile_form = BasicFormProfile(
            request.POST, instance=person.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()

        # updating the user.person
        person_form = BasicFormPerson(request.POST, instance=person)
        if person_form.is_valid():
            person_form.save()

        return redirect("person_detail", id)

    template_name = "person/forms/tab_basic.html"
    context = {
        "title": _("Update basic info"),
        "user_form": UserForm(instance=person.user),
        "profile_form": BasicFormProfile(instance=person.user.profile),
        "person_form": BasicFormPerson(
            instance=person, initial={"made_by": request.user}
        ),
        "callback_link": reverse("person_update_basic", args=[id]),
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("person.change_person")
def person_update_others(request, id):
    center_persons = [
        person.id
        for person in Person.objects.filter(
            center=request.user.person.center.pk
        )
    ]
    if id not in center_persons and not request.user.is_superuser:
        raise Http404

    person = Person.objects.get(id=id)

    if request.method == "POST":
        # updating the user.profile
        profile_form = OthersFormProfile(
            request.POST, instance=person.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()

        # updating the user.person
        person_form = OthersFormPerson(request.POST, instance=person)
        if person_form.is_valid():
            person_form.save()

        template_name = "person/elements/tab_others.html"
        return render(request, template_name, {"object": person})

    template_name = "person/forms/tab_others.html"
    context = {
        "title": _("Update others info"),
        "profile_form": OthersFormProfile(instance=person.user.profile),
        "person_form": OthersFormPerson(
            instance=person, initial={"made_by": request.user}
        ),
        "callback_link": reverse("person_update_others", args=[id]),
        "target": "tabOthers",
        "swap": "innerHTML",
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("person.change_person")
def person_update_address(request, id):
    center_persons = [
        person.id
        for person in Person.objects.filter(
            center=request.user.person.center.pk
        )
    ]
    if id not in center_persons and not request.user.is_superuser:
        raise Http404

    person = Person.objects.get(id=id)

    if request.method == "POST":
        # updating the user.profile
        profile_form = AddressFormProfile(
            request.POST, instance=person.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()

        template_name = "person/elements/tab_address.html"
        return render(request, template_name, {"object": person})

    template_name = "person/forms/tab_address.html"
    context = {
        "title": _("Update address info"),
        "profile_form": AddressFormProfile(instance=person.user.profile),
        "callback_link": reverse("person_update_address", args=[id]),
        "target": "tabAddress",
        "swap": "innerHTML",
        "update": True,
    }
    return render(request, template_name, context)


@login_required
@permission_required("person.change_person")
def person_update_image(request, id):
    center_persons = [
        person.id
        for person in Person.objects.filter(
            center=request.user.person.center.pk
        )
    ]
    if id not in center_persons and not request.user.is_superuser:
        raise Http404

    person = Person.objects.get(id=id)

    if request.method == "POST":
        # updating the user.profile
        profile_form = ImageFormProfile(
            request.POST, request.FILES, instance=person.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()

        return redirect("person_detail", id)

    template_name = "person/forms/tab_image.html"
    context = {
        "title": _("Update image info"),
        "profile_form": ImageFormProfile(instance=person.user.profile),
        "callback_link": reverse("person_update_image", args=[id]),
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
        return redirect(reverse("person_home") + "?init=on")

    context = {
        "object": person,
        "title": _("confirm to delete"),
    }

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
        "confirm_link": reverse("person_reinsert", args=[id]),
    }
    return render(request, template_name, context)


# auxiliar functions
def add_historic(person, occurrence, made_by):
    historic = dict(
        person=person,
        occurrence=occurrence,
        date=timezone.now().date(),
        made_by=made_by,
    )
    Historic.objects.create(**historic)
