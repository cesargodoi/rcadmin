import uuid

from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.db import models
from jsonfield import JSONField
from django.urls import reverse
from rcadmin.common import (
    ASPECTS,
    OCCURRENCES,
    PERSON_TYPES,
    GENDER_TYPES,
    STATUS,
    COUNTRIES,
    short_name,
    us_inter_char,
    phone_format,
)
from user.models import User


# Invitation
class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    center = models.ForeignKey(
        "center.Center",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("center"),
    )
    name = models.CharField(_("name"), max_length=80)
    birth = models.DateField(_("birth"), null=True, blank=True)
    gender = models.CharField(
        _("gender"), max_length=1, choices=GENDER_TYPES, null=True, blank=True
    )
    id_card = models.CharField(
        _("id card"), max_length=30, null=True, blank=True
    )
    address = models.CharField(_("address"), max_length=50, blank=True)
    number = models.CharField(_("number"), max_length=10, blank=True)
    complement = models.CharField(_("complement"), max_length=50, blank=True)
    district = models.CharField(_("district"), max_length=50, blank=True)
    city = models.CharField(_("city"), max_length=50, null=True, blank=True)
    state = models.CharField(_("state"), max_length=2, null=True, blank=True)
    country = models.CharField(
        _("country"), max_length=2, choices=COUNTRIES, default="BR"
    )
    zip_code = models.CharField(_("zip"), max_length=15, blank=True)
    phone = models.CharField(_("phone"), max_length=20, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    sos_contact = models.CharField(
        _("emergency contact"), max_length=50, null=True, blank=True
    )
    sos_phone = models.CharField(
        _("emergency phone"), max_length=20, null=True, blank=True
    )
    historic = JSONField(null=True, blank=True)
    observations = models.TextField(_("observations"), blank=True)
    migration = models.BooleanField(default=False)
    invited_on = models.DateTimeField(_("invited on"), default=timezone.now)
    imported = models.BooleanField(default=False)
    imported_on = models.DateTimeField(_("imported on"), null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.state:
            self.state = str(self.state).upper()
        if self.phone:
            self.phone = phone_format(self.phone)
        super(Invitation, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.name, self.center)

    class Meta:
        verbose_name = _("invitation")
        verbose_name_plural = _("invitations")


# Person
class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    center = models.ForeignKey(
        "center.Center",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("center"),
    )
    reg = models.CharField(_("reg"), max_length=10, null=True, blank=True)
    name = models.CharField(_("name"), max_length=100)
    name_sa = models.CharField(max_length=100, editable=False)
    short_name = models.CharField(
        _("short name"), max_length=80, null=True, blank=True, editable=False
    )
    id_card = models.CharField(_("id card"), max_length=30, blank=True)
    birth = models.DateField(_("birth"), null=True, blank=True)
    person_type = models.CharField(
        _("type"), max_length=3, choices=PERSON_TYPES, default="PUP"
    )
    aspect = models.CharField(
        _("aspect"), max_length=2, choices=ASPECTS, default="--"
    )
    aspect_date = models.DateField(_("date"), null=True, blank=True)
    status = models.CharField(max_length=3, choices=STATUS, default="ACT")
    observations = models.TextField(_("observations"), blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="made_by_person",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def clean(self, *args, **kwargs):
        self.is_active = (
            False if self.status not in ("ACT", "LIC", "---", "OTH") else True
        )
        super(Person, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"<<{self.user.email.split('@')[0]}>>"
        self.name_sa = us_inter_char(self.name)
        self.short_name = short_name(self.name)
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.name, self.center)

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")

    def get_absolute_url(self):
        return reverse("person_detail", kwargs={"id": self.id})


# Historic
class Historic(models.Model):
    person = models.ForeignKey(
        Person, on_delete=models.PROTECT, verbose_name=_("person")
    )
    occurrence = models.CharField(
        _("occurrence"), max_length=3, choices=OCCURRENCES, default="ACT"
    )
    date = models.DateField(_("date"), null=True, blank=True)
    description = models.CharField(
        _("description"), max_length=200, null=True, blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="made_by_historic",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"[{self.date}] {self.person.name} - {self.occurrence}"

    class Meta:
        verbose_name = _("historic")
        verbose_name_plural = _("historics")
