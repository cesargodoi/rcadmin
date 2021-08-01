import re
from unicodedata import normalize

from django import forms
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import Http404
from django.core.validators import RegexValidator


# hidden auth fields
HIDDEN_AUTH_FIELDS = {
    "is_active": forms.HiddenInput(),
    "created_on": forms.HiddenInput(),
    "modified_on": forms.HiddenInput(),
    "made_by": forms.HiddenInput(),
}

# choices for some fields
GENDER_TYPES = (("M", "male"), ("F", "female"))
CENTER_TYPES = (
    ("CNT", "center"),
    ("CNF", "conference center"),
    ("CTT", "contact room"),
)
ASPECTS = (
    ("--", "--"),
    ("A1", "1st. Aspect"),
    ("A2", "2nd. Aspect"),
    ("A3", "3rd. Aspect"),
    ("A4", "4th. Aspect"),
    ("GR", "Grail"),
    ("A5", "5th. Aspect"),
    ("A6", "6th. Aspect"),
)
STATUS = (
    ("---", "---"),
    ("ACT", "active"),
    ("LIC", "licensed"),
    ("DEA", "dead"),
    ("DIS", "disconnected"),
    ("REM", "removed"),
)
OCCURRENCES = (
    ("TRF", "transfered"),
    ("RGS", "regressed"),
    ("OTH", "other"),
    ("PRP", "preparatório"),
    ("PRB", "probatório"),
    ("PRF", "professo"),
)
OCCURRENCES += ASPECTS
OCCURRENCES += STATUS
PERSON_TYPES = (("PUP", "pupil"), ("WEB", "web pupil"), ("GST", "gest"))
ROLE_TYPES = (("MTR", "mentor"), ("CTT", "contact"), ("MBR", "member"))
WORKGROUP_TYPES = (("ASP", "aspect"), ("MNT", "maintenance"), ("ADM", "admin"))
EVENT_STATUS = (("OPN", "open"), ("CLS", "close"))
ACTIVITY_TYPES = (
    ("SRV", "service"),
    ("CNF", "conference"),
    ("MET", "meeting"),
    ("OTH", "other"),
)
ORDER_STATUS = (
    ("CCL", "canceled"),
    ("PND", "pending"),
    ("CCD", "concluded"),
)
PAY_TYPES = (
    ("MON", "monthly"),
    ("EVE", "by event"),
    ("CAM", "campaign"),
)
PAYFORM_TYPES = (
    ("PIX", "pix"),
    ("CSH", "cash"),
    ("CHK", "check"),
    ("PRE", "pre check"),
    ("DBT", "debit"),
    ("CDT", "credit"),
    ("DPT", "deposit"),
    ("TRF", "transfer"),
    ("SLP", "bank slip"),
)
PROFILE_PAYFORM_TYPES = (
    ("PIX", "pix"),
    ("DPT", "deposit"),
    ("TRF", "transfer"),
)
COUNTRIES = (("BR", "Brasil"),)
LECTURE_TYPES = (("CTT", "contact"), ("MET", "meeting"))
SEEKER_STATUS = (
    ("OBS", "observation"),
    ("NEW", "new"),
    ("MBR", "member"),
    ("RCP", "reception"),
    ("INS", "installing"),
    ("RST", "restriction"),
)
BR_REGIONS = {
    "SP": ["SP"],
    "RJ": ["RJ", "ES"],
}


def us_inter_char(txt, codif="utf-8"):
    if not isinstance(txt, str):
        txt = str(txt)
    return (
        normalize("NFKD", txt)
        .encode("ASCII", "ignore")
        .decode("ASCII")
        .lower()
    )


def short_name(name):
    name = name.split(" ")
    words = [word for word in name if len(word) > 3]
    to_join = []
    if len(words) >= 3:
        for n, word in enumerate(words):
            if n == 0:
                to_join.append(word)
            if n == 1:
                to_join.append(f"{word[0]}.")
            if n == len(words) - 1:
                to_join.append(word)
    else:
        to_join = words
    return " ".join(to_join)


def cpf_validation(num):
    cpf = "".join(re.findall(r"\d", num))

    if len(cpf) != 11:
        return False
    if cpf in (
        "00000000000",
        "11111111111",
        "22222222222",
        "33333333333",
        "44444444444",
        "55555555555",
        "66666666666",
        "77777777777",
        "88888888888",
        "99999999999",
    ):
        return False

    weight1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    digit1 = 11 - (
        sum([int(d) * weight1[n] for n, d in enumerate(cpf[:9])]) % 11
    )
    if digit1 > 9:
        digit1 = 0

    if cpf[9:10] != f"{digit1}":
        return False

    weight2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    digit2 = 11 - (
        sum([int(d) * weight2[n] for n, d in enumerate(cpf[:9] + str(digit1))])
        % 11
    )
    if digit2 > 9:
        digit2 = 0

    if cpf[9:] != f"{digit1}{digit2}":
        return False

    return True


def cpf_format(num):
    cpf = "".join(re.findall(r"\d", num))
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be entered in the format: '+999999999'. \
        Up to 15 digits allowed.",
)


def phone_format(num, country="BR"):
    num = (
        "+{}".format("".join(re.findall(r"\d", num)))
        if num.startswith("+")
        else "".join(re.findall(r"\d", num))
    )

    if not num:
        return ""

    if country == "BR":
        if num.startswith("+"):
            num = (
                f"+{num[1:3]} {num[3:5]} {num[5:10]}-{num[10:]}"
                if len(num) == 14
                else f"+{num[1:3]} {num[3:5]} {num[5:9]}-{num[9:]}"
            )
        elif len(num) in (10, 11):
            num = (
                f"+55 {num[:2]} {num[2:7]}-{num[7:]}"
                if len(num) == 11
                else f"+55 {num[:2]} {num[2:6]}-{num[6:]}"
            )

    return num


def paginator(queryset, limit=10, page=1):
    paginator = Paginator(queryset, limit)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    return object_list


def belongs_center(request, pk, obj):
    object_list = [
        pk.pk
        for pk in obj.objects.filter(center=request.user.person.center.id)
    ]
    if pk not in object_list and not request.user.is_superuser:
        raise Http404


def clear_session(request, items):
    for item in items:
        if request.session.get(item):
            del request.session[item]


def send_email(
    body_text,
    body_html,
    _subject,
    _to,
    _from="no-reply@rosacruzaurea.org.br",
    _context={},
):
    text_content = render_to_string(body_text, _context)
    html_content = render_to_string(body_html, _context)

    subject = f"Rosacruz Áurea - {_subject}"

    send_mail(
        subject=subject,
        from_email=_from,
        message=text_content,
        recipient_list=[_to],
        html_message=html_content,
        fail_silently=True,
    )


def get_filename(instance, field=None):
    if field:
        if field == "pix_key":
            temp = "{} {}".format(
                us_inter_char(instance.short_name),
                instance.__getattribute__(field),
            )
        else:
            temp = us_inter_char(instance.__getattribute__(field))
        _name = re.sub(r"[^\w\s]", "", temp)
    else:
        _name = us_inter_char(instance.name)
    ext = instance.image.name.split(".")[-1]
    name = "-".join(_name.split())
    return f"{name}.{ext}"
