import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from schooladmin.common import (
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
    )
    reg = models.CharField(max_length=10)
    name = models.CharField(max_length=80)
    name_sa = models.CharField(max_length=80, editable=False)
    short_name = models.CharField(max_length=40, null=True, blank=True)
    id_card = models.CharField("id card", max_length=20, blank=True)
    birth = models.DateField(null=True, blank=True)
    person_type = models.CharField(
        "type", max_length=3, choices=PERSON_TYPES, default="PUP"
    )
    aspect = models.CharField(max_length=2, choices=ASPECTS, default="--")
    aspect_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=3, choices=STATUS, default="ACT")
    observations = models.TextField(blank=True)
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
            False if self.status not in ("ACT", "LIC", "---") else True
        )
        super(Person, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = (
                f"<<{self.user.email.split('@')[0]}>> REQUIRES ADJUSTMENTS"
            )
        self.name_sa = us_inter_char(self.name)
        self.short_name = short_name(self.name)
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.name, self.center)

    class Meta:
        verbose_name = "person"
        verbose_name_plural = "persons"

    def get_absolute_url(self):
        return reverse("person_detail", kwargs={"id": self.id})


# Historic
class Historic(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    occurrence = models.CharField(
        max_length=3, choices=OCCURRENCES, default="ACT"
    )
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
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
        verbose_name = "historic"
        verbose_name_plural = "historics"
