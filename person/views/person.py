from datetime import date

from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.urls import reverse

from schooladmin.common import ASPECTS, STATUS, paginator, clear_session
from user.models import User
from base.searchs import search_person

from ..forms import PersonForm, ProfileForm, UserForm
from ..models import Historic, Person


@login_required
@permission_required("person.view_person")
def person_home(request):
    object_list = None
    if request.GET.get("init"):
        clear_session(request, ["search"])
    else:
        queryset, page = search_person(request, Person)
        object_list = paginator(queryset, page=page)
        # add action links
        for item in object_list:
            item.click_link = reverse("person_detail", args=[item.id])

    context = {
        "object_list": object_list,
        "init": True if request.GET.get("init") else False,
        "aspect_list": ASPECTS,
        "status_list": STATUS,
        "title": "person home",
        "nav": "home",
        "flag": "person",
    }
    return render(request, "person/person_home.html", context)


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
        "title": "person detail",
        "person": person,  # to header element
        "age": age,
        "nav": "detail",
        "tab": "info",
        "date": timezone.now().date(),
    }
    return render(request, "person/person_detail.html", context)


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
        "title": "create person",
        "to_create": True,
    }
    return render(request, "base/form.html", context)


@login_required
@permission_required("person.change_person")
def person_update(request, id):
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
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=person.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()

        # updating the user.person
        person_form = PersonForm(request.POST, instance=person)
        if person_form.is_valid():
            person_form.save()
            message = f"The Person '{request.POST['name']}' has been updated!"
            messages.success(request, message)

        return redirect("person_detail", id=id)

    user_form = UserForm(instance=person.user)
    profile_form = ProfileForm(instance=person.user.profile)
    person_form = PersonForm(
        instance=person, initial={"made_by": request.user}
    )

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "person_form": person_form,
        "form_name": "Person",
        "form_path": "person/forms/person.html",
        "goback": reverse("person_detail", args=[id]),
        "title": "update person",
        "id": id,
    }
    return render(request, "base/form.html", context)


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

    context = {"object": person, "title": "confirm to delete"}
    return render(request, "base/confirm_delete.html", context)


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
        return redirect(reverse("person_home") + "?init=on")

    context = {"object": person, "title": "confirm to reinsert"}
    return render(
        request, "person/elements/confirm_to_reinsert_person.html", context
    )


# auxiliar functions
def add_historic(person, occurrence, made_by):
    historic = dict(
        person=person,
        occurrence=occurrence,
        date=timezone.now().date(),
        made_by=made_by,
    )
    Historic.objects.create(**historic)


# @login_required
# @permission_required("person.add_person")
# def person_create(request):
#     if request.method == "POST":
#         # creating a new user
#         password = BaseUserManager().make_random_password()
#         if request.POST.get("email"):
#             email = request.POST["email"]
#             new_user = User.objects.create_user(
#                 email=email,
#                 password=password,
#             )
#             # updating the user.profile
#             profile_form = ProfileForm(
#                 request.POST, request.FILES, instance=new_user.profile
#             )
#             if profile_form.is_valid():
#                 profile_form.save()
#             # updating the user.person
#             person_form = PersonForm(request.POST, instance=new_user.person)
#             if person_form.is_valid():
#                 person_form.save()
#             # add password in observations
#             new_user.person.observations += f"\nfirst password: {password}"
#             # the center is the same as the center of the logged in user
#             new_user.person.center = request.user.person.center
#             new_user.person.save()
#             message = f"The Person '{request.POST['name']}' has been created!"
#             messages.success(request, message)
#             return redirect("person_detail", id=new_user.person.pk)
#         else:
#             message = "Enter a valid email!"
#             messages.warning(request, message)

#     user_form = UserForm()
#     profile_form = ProfileForm()
#     person_form = PersonForm(initial={"made_by": request.user})

#     context = {
#         "user_form": user_form,
#         "profile_form": profile_form,
#         "person_form": person_form,
#         "form_name": "Person",
#         "form_path": "person/forms/person.html",
#         "goback": reverse("person_home"),
#         "title": "create person",
#         "to_create": True,
#     }
#     return render(request, "base/form.html", context)
