import uuid

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.urls import reverse
from rcadmin.common import (
    ASPECTS,
    OCCURRENCES,
    PERSON_TYPES,
    STATUS,
    short_name,
    us_inter_char,
)
from user.models import User


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
        verbose_name_plural = _("persons")

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
