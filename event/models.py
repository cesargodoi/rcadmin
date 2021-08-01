import uuid
from io import BytesIO

import qrcode
from django.conf import settings
from django.core.files import File
from django.db import models
from PIL import Image
from schooladmin.common import ACTIVITY_TYPES, EVENT_STATUS, ASPECTS
from person.models import Person


#  Activity
class Activity(models.Model):
    name = models.CharField(max_length=50)
    activity_type = models.CharField(
        "type", max_length=3, choices=ACTIVITY_TYPES, default="SRV"
    )
    multi_date = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "activity"
        verbose_name_plural = "activities"


#  Event
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity = models.ForeignKey(Activity, on_delete=models.PROTECT)
    qr_code = models.ImageField(upload_to="event_qr_codes", blank=True)
    center = models.ForeignKey("center.Center", on_delete=models.PROTECT)
    date = models.DateField(null=True, blank=True)
    end_date = models.DateField("end", null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=3, choices=EVENT_STATUS, default="OPN"
    )
    description = models.CharField(max_length=200, null=True, blank=True)
    frequencies = models.ManyToManyField(
        Person, through="Frequency", blank=True
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
        verbose_name = "event"
        verbose_name_plural = "events"
        ordering = ["date"]


#  Frequency
class Frequency(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    aspect = models.CharField(max_length=2, choices=ASPECTS, default="--")
    ranking = models.IntegerField(default=0)
    observations = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "event: {} person: {} asp: {} rank: {}".format(
            self.event, self.person, self.aspect, self.ranking
        )

    class Meta:
        verbose_name = "frequency"
        verbose_name_plural = "frequencies"
