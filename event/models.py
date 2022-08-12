import uuid
import qrcode

from io import BytesIO

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.files import File
from django.db import models
from PIL import Image
from rcadmin.common import ACTIVITY_TYPES, EVENT_STATUS, ASPECTS
from person.models import Person


#  Activity
class Activity(models.Model):
    name = models.CharField(_("name"), max_length=50)
    activity_type = models.CharField(
        _("type"), max_length=3, choices=ACTIVITY_TYPES, default="SRV"
    )
    multi_date = models.BooleanField(_("multi date"), default=False)
    is_active = models.BooleanField(_("active"), default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")


#  Event
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity = models.ForeignKey(
        Activity, on_delete=models.PROTECT, verbose_name=_("activity")
    )
    qr_code = models.ImageField(
        _("qr code"), upload_to="event_qr_codes", blank=True
    )
    center = models.ForeignKey(
        "center.Center", on_delete=models.PROTECT, verbose_name=_("center")
    )
    date = models.DateField(
        _("date"),
    )
    end_date = models.DateField(_("end"), null=True, blank=True)
    deadline = models.DateTimeField(_("dead line"), null=True, blank=True)
    status = models.CharField(
        max_length=3, choices=EVENT_STATUS, default="OPN"
    )
    description = models.CharField(
        _("description"), max_length=200, null=True, blank=True
    )
    frequencies = models.ManyToManyField(
        Person, through="Frequency", blank=True, verbose_name=_("frequencies")
    )
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_event",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.activity} - {self.center} ({self.date})"

    def save(self, *args, **kwargs):
        # generating QR
        if not self.qr_code:
            qr_img = qrcode.make(self.id)
            canvas = Image.new("RGB", (370, 370), "white")
            canvas.paste(qr_img)
            file_name = f"{self.id}.png"
            buffer = BytesIO()
            canvas.save(buffer, "PNG")
            self.qr_code.save(file_name, File(buffer), save=False)
            canvas.close()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ["date"]


#  Frequency
class Frequency(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.PROTECT, verbose_name=_("event")
    )
    person = models.ForeignKey(
        Person, on_delete=models.PROTECT, verbose_name=_("person")
    )
    aspect = models.CharField(
        _("aspect"), max_length=2, choices=ASPECTS, default="--"
    )
    ranking = models.IntegerField(_("ranking"), default=0)
    observations = models.CharField(
        _("observations"), max_length=100, null=True, blank=True
    )

    def __str__(self):
        return "event: {} person: {} asp: {} rank: {}".format(
            self.event, self.person, self.aspect, self.ranking
        )

    class Meta:
        verbose_name = _("frequency")
        verbose_name_plural = _("frequencies")
