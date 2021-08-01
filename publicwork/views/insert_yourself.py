import requests

from datetime import datetime, timedelta

from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings

from user.models import User
from center.models import Center
from ..forms import TempRegOfSeekerForm
from ..models import TempRegOfSeeker, Seeker
from schooladmin.common import clear_session, send_email


def insert_yourself(request):
    clear_session(request, ["fbk"])
    if request.method == "POST":
        # reCAPTCHA validation
        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        }
        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify", data=data
        )
        result = r.json()
        # if reCAPTCHA returns False
        if not result["success"]:
            request.session["fbk"] = {"type": "recaptcha"}
            return redirect("feedback")

        # checking if the email has already been used in the User
        if User.objects.filter(email=request.POST.get("email")):
            request.session["fbk"] = {
                "type": "pupil",
                "email": request.POST.get("email"),
            }
            return redirect("feedback")

        # checking if the email has already been used in the Seeker
        if Seeker.objects.filter(email=request.POST.get("email")):
            request.session["fbk"] = {
                "type": "seeker",
                "email": request.POST.get("email"),
            }
            return redirect("feedback")

        # checking if the email has already been used in the TempRegOfSeeker
        if TempRegOfSeeker.objects.filter(email=request.POST.get("email")):
            request.session["fbk"] = {
                "type": "email",
                "email": request.POST.get("email"),
            }
            return redirect("feedback")

        # populating form with request.POST
        form = TempRegOfSeekerForm(request.POST, request.FILES)

        if form.is_valid():
            # save form data in TempRegOfSeeker table
            form.save()
            # get temp_seeker using email (in form cleaned_data)
            _seeker = TempRegOfSeeker.objects.get(
                email=form.cleaned_data.get("email")
            )
            # send email
            _link = "{}://{}{}".format(
                "http",
                "localhost:8000",
                reverse("confirm_email", args=[_seeker.id]),
            )
            send_email(
                body_text="publicwork/insert_yourself/emails/to_confirm.txt",
                body_html="publicwork/insert_yourself/emails/to_confirm.html",
                _subject="confirmação de email",
                _to=_seeker.email,
                _context={"name": _seeker.name, "link": _link},
            )

        request.session["fbk"] = {
            "type": "email",
            "email": request.POST.get("email"),
        }
        return redirect("feedback")

    context = {
        "form": TempRegOfSeekerForm(),
        "recaptcha_site_key": settings.GOOGLE_RECAPTCHA_SITE_KEY,
        "form_name": "Seeker",
        "form_path": "publicwork/forms/seeker.html",
        "goback": reverse("seeker_home"),
        "title": "create seeker",
        "to_create": True,
    }
    return render(request, "publicwork/insert_yourself/form.html", context)


def feedback(request):
    context = {"title": "insert yourself as a seeker"}
    return render(
        request, "publicwork/insert_yourself/form_feedback.html", context
    )


def confirm_email(request, token):
    _seeker = get_object_or_404(TempRegOfSeeker, pk=token)
    # get dates
    time_now = datetime.utcnow()
    token_time = _seeker.solicited_on.replace(tzinfo=None) + timedelta(hours=6)

    if time_now < token_time:
        new_seeker = dict(
            center=get_seeker_center(_seeker),
            name=_seeker.name,
            birth=_seeker.birth,
            gender=_seeker.gender,
            image=_seeker.image,
            city=_seeker.city,
            state=_seeker.state,
            country=_seeker.country,
            phone=_seeker.phone,
            email=_seeker.email,
        )
        # create new seeker
        Seeker.objects.create(**new_seeker)
        # send congratulations email
        send_email(
            body_text="publicwork/insert_yourself/emails/to_congratulate.txt",
            body_html="publicwork/insert_yourself/emails/to_congratulate.html",
            _subject="cadastro realizado",
            _to=_seeker.email,
            _context={"name": _seeker.name},
        )
        # pass context to feedbak
        context = {"feedback": "congratulations"}
        # delete temp seeker
        _seeker.delete()
    else:
        context = {"feedback": "token_expires"}

    return render(
        request, "publicwork/insert_yourself/pos_email_feedback.html", context
    )


# handlers
def get_seeker_center(seeker):
    city = seeker.city
    state = seeker.state
    country = seeker.country

    try:
        center = Center.objects.get(city=city, state=state, country=country)
    except Exception:
        center = (
            Center.objects.filter(state=state, country=country)
            .order_by("created_on")
            .first()
        )
    except Exception:
        center = (
            Center.objects.filter(country=country)
            .order_by("created_on")
            .first()
        )
    except Exception:
        center = Center.objects.get(name="Web Core")

    return center
