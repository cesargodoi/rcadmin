import requests
import json

from datetime import date, datetime, timedelta
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.http.request import QueryDict
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from rcadmin.common import (
    clear_session,
    get_pagination,
    send_email,
    sanitize_name,
)
from base.searchs import search_invitations

from ..views.historic import adjust_person_side
from ..models import Invitation, Person, Historic
from ..forms import InvitationForm, PupilRegistrationForm
from publicwork.models import Seeker
from user.models import User

modal_updated_triggers = json.dumps(
    {
        "closeModal": True,
        "showToast": _("The Invitation has been sent!"),
    }
)


@login_required
@permission_required("person.view_invitation")
def invitations(request):
    clear_session(request, ["search"])
    context = {"title": _("invitations"), "nav": "invitations"}
    return render(request, "person/home.html", context)


def invite_list(request):
    page, _from, _to, LIMIT = get_pagination(request)

    if request.GET.get("clear") or not request.GET.get("ps_term"):
        clear_session(request, ["search"])

    object_list, count = search_invitations(request, Invitation, _from, _to)
    for item in object_list:
        item.del_link = reverse("remove_invite", args=[item.pk])
        item.resend_invitation = reverse(resend_invitation, args=[item.pk])

    template_name = "person/invitation/elements/invite_list.html"
    context = {
        "LIMIT": LIMIT,
        "page": page,
        "counter": (page - 1) * LIMIT,
        "object_list": object_list,
        "count": count,
        "clear_search": True if request.GET.get("clear") else False,
    }
    return HttpResponse(render_to_string(template_name, context, request))


@login_required
@permission_required("person.add_invitation")
def invite(request):
    if request.method == "POST":
        data = QueryDict(request.body).dict()
        form = InvitationForm(data)
        msg = ""
        if User.objects.filter(email=data["email"]):
            msg = f"{data['name']} is already a pupil."
        elif Invitation.objects.filter(email=data["email"]):
            msg = f"{data['email']} has already been invited."
        elif Seeker.objects.filter(email=data["email"]):
            msg = "{} is already a 'seeker'.\nUse import from Seekers.".format(
                data["name"]
            )
        else:
            if form.is_valid():
                new_invite = form.save()
                new_invite.historic = {"A1": str(date.today())}
                new_invite.save()
                send_invitation(request, new_invite)
                return redirect("invitations")

        return HttpResponse(
            headers={
                "HX-Retarget": "#formBody",
                "HX-Trigger": json.dumps(
                    {
                        "closeModal": True,
                        "showToast": msg,
                    }
                ),
            },
        )

    else:
        form = InvitationForm(initial={"center": request.user.person.center})

    template_name = "person/invitation/forms/invite_pupil.html"
    context = {
        "form": form,
        "title": _("Invite new pupil"),
    }
    return render(request, template_name, context)


def send_invitation(request, invite):
    address = "https://rcadmin.rosacruzaurea.org.br"
    _link = f"{address}{reverse('confirm_invitation', args=[invite.pk])}"
    action = "migration" if invite.migration else "invitation"
    send_email(
        body_text=f"person/invitation/emails/confirm_{action}.txt",
        body_html=f"person/invitation/emails/confirm_{action}.html",
        _subject="Convite para ser aluno",
        _to=invite.email,
        _context={
            "name": invite.name,
            "center": invite.center.name,
            "email": invite.email,
            "link": _link,
        },
    )


@login_required
@permission_required("person.delete_invitation")
def remove_invite(request, pk):
    invite = Invitation.objects.get(pk=pk)
    if request.method == "POST":
        invite.delete()
        return redirect("invitations")

    template_name = "person/invitation/confirm/delete.html"
    context = {"object": "{} ⛔️ {}".format(invite.name, invite.center)}
    return render(request, template_name, context)


@login_required
@permission_required("person.add_invitation")
def resend_invitation(request, pk):
    invite = Invitation.objects.get(pk=pk)
    if request.method == "POST":
        invite.invited_on = datetime.now()
        invite.save()
        send_invitation(request, invite)
        return redirect("invitations")

    template_name = "person/invitation/confirm/resend_invitation.html"
    context = {"object": "{} ➜ {}".format(invite.name, invite.center)}
    return render(request, template_name, context)


def reg_feedback(request):
    context = {"title": _("pupil registration")}
    return render(request, "person/invitation/form_feedback.html", context)


def confirm_invitation(request, token):
    try:
        invite = Invitation.objects.get(pk=token)
    except Exception:
        # lost invitation
        request.session["fbk"] = {"type": "lost_invitation"}
        return redirect("reg_feedback")

    # already imported
    if invite.imported:
        request.session["fbk"] = {
            "type": "already_imported",
            "name": invite.name,
            "imported_on": str(invite.imported_on),
        }
        return redirect("reg_feedback")

    # compare token date (1 day)
    token_time = invite.invited_on.replace(tzinfo=None) + timedelta(days=1)
    if datetime.utcnow() > token_time:
        request.session["fbk"] = {"type": "expired_token"}
        return redirect("reg_feedback")

    template_name = "person/invitation/forms/data_registration.html"

    if request.method == "POST":
        # TODO - descomentar as linhas abaixo
        # # reCAPTCHA validation
        # recaptcha_response = request.POST.get("g-recaptcha-response")
        # data = {
        #     "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        #     "response": recaptcha_response,
        # }
        # r = requests.post(
        #     "https://www.google.com/recaptcha/api/siteverify", data=data
        # )
        # result = r.json()
        # # if reCAPTCHA returns False
        # if not result["success"]:
        #     request.session["fbk"] = {"type": "recaptcha"}
        #     return redirect("reg_feedback")

        # populating the form
        form = PupilRegistrationForm(request.POST, instance=invite)
        # using the data
        data = request.POST.dict()

        # update or create user
        if invite.sign_lgpd:
            # update user
            user = User.objects.get(email=invite.email)
            user.set_password(data["password"])
            # updating the user.profile
            user.profile.social_name = sanitize_name(data["name"])
            user.profile.gender = data["gender"]
            user.profile.city = data["city"]
            user.profile.state = data["state"]
            user.profile.country = data["country"]
            user.profile.phone = data["phone"]
            user.profile.sos_contact = sanitize_name(data["sos_contact"])
            user.profile.sos_phone = data["sos_phone"]
            user.profile.save()
            # updating the user.person
            user.person.name = invite.name
            user.person.center = invite.center
            user.person.id_card = data["id_card"]
            user.person.birth = datetime.strptime(data["birth"], "%Y-%m-%d")
            user.is_active = True
            user.save()
            user.person.is_active = True
            user.person.save()
        else:
            # creating a new user
            user = User.objects.create_user(
                email=invite.email, password=data["password"]
            )
            # add user in "user" group
            user.groups.add(Group.objects.get(name="user"))
            # updating the user.profile
            user.profile.social_name = sanitize_name(data["name"])
            user.profile.gender = data["gender"]
            user.profile.city = data["city"]
            user.profile.state = data["state"]
            user.profile.country = data["country"]
            user.profile.phone = data["phone"]
            user.profile.sos_contact = sanitize_name(data["sos_contact"])
            user.profile.sos_phone = data["sos_phone"]
            user.profile.save()
            # updating the user.person
            user.person.name = invite.name
            user.person.center = invite.center
            user.person.id_card = data["id_card"]
            user.person.birth = datetime.strptime(data["birth"], "%Y-%m-%d")
            user.person.save()
            # add historic - Aspect 'A1'
            aspect, _date = tuple(invite.historic.items())[0]
            date = datetime.strptime(_date, "%Y-%m-%d")
            Historic.objects.create(
                person=user.person, occurrence=aspect, date=date
            )
            adjust_person_side(user.person, aspect, date)

        # update invite imported
        invite.imported = True
        invite.imported_on = datetime.now()
        invite.save()

        # send congratulations email
        send_email(
            body_text="person/invitation/emails/to_congratulate.txt",
            body_html="person/invitation/emails/to_congratulate.html",
            _subject="cadastro realizado",
            _to=invite.email,
            _context={"object": invite},
        )

        return redirect("congratulations", pk=invite.pk)

    else:
        form = PupilRegistrationForm(instance=invite)

    context = {
        "form": form,
        "total_address": True if "A1" not in invite.historic.keys() else False,
        "title": _("create pupil"),
        "rca_logo": True,
    }
    return render(request, template_name, context)


def congratulations(request, pk):
    template_name = "person/invitation/congratulations.html"
    context = {
        "title": _("congratulations"),
        "object": Invitation.objects.get(pk=pk),
    }
    return render(request, template_name, context)
