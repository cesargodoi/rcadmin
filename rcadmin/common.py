import re
import pandas as pd

from io import StringIO
from unicodedata import normalize

from django import forms
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import Http404
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _


# hidden auth fields
HIDDEN_AUTH_FIELDS = {
    "is_active": forms.HiddenInput(),
    "created_on": forms.HiddenInput(),
    "modified_on": forms.HiddenInput(),
    "made_by": forms.HiddenInput(),
}

GRC = _("Golden Rosycross")

# choices for some fields
GENDER_TYPES = (
    ("M", _("male")),
    ("F", _("female")),
)
CENTER_TYPES = (
    ("CNT", _("center")),
    ("CNF", _("conference center")),
    ("CTT", _("contact room")),
)
ASPECTS = (
    ("--", "--"),
    ("A1", _("1st. Aspect")),
    ("A2", _("2nd. Aspect")),
    ("A3", _("3rd. Aspect")),
    ("A4", _("4th. Aspect")),
    ("GR", _("Grail")),
    ("A5", _("5th. Aspect")),
    ("A6", _("6th. Aspect")),
)
STATUS = (
    ("---", "---"),
    ("ACT", _("active")),
    ("LIC", _("licensed")),
    ("DEA", _("dead")),
    ("DIS", _("disconnected")),
    ("REM", _("removed")),
)
OCCURRENCES = (
    ("TRF", _("transfered")),
    ("RGS", _("regressed")),
    ("OTH", _("other")),
    ("PRP", _("preparatório")),
    ("PRB", _("probatório")),
    ("PRF", _("professo")),
)
OCCURRENCES += ASPECTS
OCCURRENCES += STATUS
PERSON_TYPES = (
    ("PUP", _("pupil")),
    ("WEB", _("web pupil")),
    ("GST", _("gest")),
)
ROLE_TYPES = (
    ("MTR", _("mentor")),
    ("CTT", _("contact")),
    ("MBR", _("member")),
)
WORKGROUP_TYPES = (
    ("ASP", _("aspect")),
    ("MNT", _("maintenance")),
    ("ADM", _("admin")),
)
EVENT_STATUS = (
    ("OPN", _("open")),
    ("CLS", _("close")),
)
ACTIVITY_TYPES = (
    ("SRV", _("service")),
    ("CNF", _("conference")),
    ("MET", _("meeting")),
    ("OTH", _("other")),
)
ORDER_STATUS = (
    ("CCL", _("canceled")),
    ("PND", _("pending")),
    ("CCD", _("concluded")),
)
PAY_TYPES = (
    ("MON", _("monthly")),
    ("EVE", _("by event")),
    ("CAM", _("campaign")),
)
PAYFORM_TYPES = (
    ("PIX", _("pix")),
    ("CSH", _("cash")),
    ("CHK", _("check")),
    ("PRE", _("pre check")),
    ("DBT", _("debit")),
    ("CDT", _("credit")),
    ("DPT", _("deposit")),
    ("TRF", _("transfer")),
    ("SLP", _("bank slip")),
)
PROFILE_PAYFORM_TYPES = (
    ("PIX", _("pix")),
    ("DPT", _("deposit")),
    ("TRF", _("transfer")),
)
COUNTRIES = (("BR", _("Brazil")),)
LECTURE_TYPES = (
    ("CTT", _("contact")),
    ("MET", _("meeting")),
)
SEEKER_STATUS = (
    ("OBS", _("observation")),
    ("NEW", _("new")),
    ("MBR", _("member")),
    ("INS", _("installing")),
    ("ITD", _("installed")),
    ("STD", _("stand by")),
    ("RST", _("restriction")),
)
BR_REGIONS = {
    "SP": ["SP"],
    "RJ": ["RJ", "ES"],
}


def sanitize_name(name):
    return " ".join([w.lower().capitalize() for w in name.split()])


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
    words = name.split(" ")
    if len(words) <= 2:
        return name
    # get first and last words of name
    first_word = words[0]
    words.pop(0)
    last_word = words[-1]
    words.pop()
    # make a list to join
    to_join = [first_word]
    for word in words:
        if len(word) <= 3:
            to_join.append(word.lower())
        else:
            to_join.append(f"{word[0]}.")
    to_join.append(last_word)
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
    message=_(
        "Phone number must be entered in the format: '+1234567890'. \
            Up to 15 digits allowed."
    ),
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

    subject = f"{GRC} - {_subject}"

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


#  sanitize csv ###############################################################
# lists to sanitize class
DEFAULT_COLUMNS = [
    "reg",
    "name",
    "gender",
    "birth",
    "__full_address",
    "district",
    "city",
    "state_prov",
    "zip",
    "country",
    "rg",
    "exp",
    "cpf",
    "phone",
    "cell_phone",
    "email",
    "profession",
    "sos_contact",
    "sos_phone",
    "ps",
    "A1",
    "A2",
    "A3",
    "A4",
    "GR",
    "A5",
    "A6",
]

DEFAULT_DATES = ["birth", "A1", "A2", "A3", "A4", "GR", "A5", "A6"]


class SanitizeCsv:
    def __init__(
        self,
        file,
        path,
        columns=DEFAULT_COLUMNS,
        dates=DEFAULT_DATES,
        fields=False,
    ):
        self.file = file
        self.path = path
        self.columns = columns
        self.dates = dates
        self.objs = [
            col for col in columns if col not in dates and col != "email"
        ]
        self.fields = fields
        self.df = self.get_dataframe

    @property
    def get_dataframe(self):
        df = pd.read_csv(
            StringIO(self.file.read().decode("utf-8")),
            parse_dates=self.dates,
            dtype={k: object for k in self.objs},
        )
        for column in self.columns:
            if column not in df.columns:
                return False
        return df[self.columns]

    def adjust_data(self):
        # remove NaN
        for _obj in self.objs:
            self.df[_obj] = self.df[_obj].fillna("")
        # split __full_address in address, number, complement
        if "__full_address" in self.df.columns:
            self.df[["address", "number", "complement"]] = (
                self.df["__full_address"]
                .str.split(",", expand=True)
                .fillna("")
            )
        # clear phones
        phones = [_ph for _ph in self.columns if "phone" in _ph]
        if phones:
            for phone in phones:
                self.df[phone] = (
                    self.df[phone]
                    .apply(lambda x: self.clear_phone(x))
                    .fillna("")
                )

    def generate_files(self):
        if self.fields:
            self.df.to_csv(f"{self.path}/fields__{self.file}")
        elif self.df["email"].isnull().sum() > 0:
            without_email = self.df.loc[self.df["email"].isna()]
            without_email_path = f"{self.path}/without_email/we__{self.file}"
            without_email.reset_index(drop=True).to_csv(without_email_path)

            with_email = self.df.drop(without_email.index)
            with_email_path = f"{self.path}/{self.file}"
            with_email.reset_index(drop=True).to_csv(with_email_path)
        else:
            self.df.to_csv(f"{self.path}/{self.file}")

    @staticmethod
    def clear_phone(phone):
        if isinstance(phone, str):
            return "".join(re.findall(r"\d*", phone))
        return phone
