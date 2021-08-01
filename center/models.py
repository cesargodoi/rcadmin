import uuid

from django.conf import settings
from django.db import models
from PIL import Image
from schooladmin.common import (
    get_filename,
    phone_format,
    CENTER_TYPES,
    COUNTRIES,
)


def center_pics(instance, filename):
    filename = get_filename(instance)
    return f"center_pics/{filename}"


def center_pix_pics(instance, filename):
    filename = get_filename(instance, field="pix_key")
    return f"center_pix_pics/{filename}"


# Center
class Center(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=25, null=True, blank=True)
    address = models.CharField(max_length=50, blank=True)
    number = models.CharField(max_length=10, blank=True)
    complement = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField("state", max_length=2, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRIES, default="BR")
    zip_code = models.CharField("zip code", max_length=15, blank=True)
    phone_1 = models.CharField("phone", max_length=20, blank=True)
    phone_2 = models.CharField("backup phone", max_length=20, blank=True)
    email = models.CharField(max_length=60, blank=True)
    secretary = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="secretary",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        default="default_center.jpg", upload_to=center_pics, blank=True
    )
    pix_image = models.ImageField(
        default="default_center_pix.jpg", upload_to=center_pix_pics, blank=True
    )
    pix_key = models.CharField(
        max_length=50, unique=True, null=True, blank=True
    )
    center_type = models.CharField(
        "type", max_length=3, choices=CENTER_TYPES, default="CNT"
    )
    conf_center = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True
    )
    observations = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="made_by_center",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.state = str(self.state).upper()
        self.phone_1 = phone_format(self.phone_1)
        self.phone_2 = phone_format(self.phone_2)
        super(Center, self).save(*args, **kwargs)
        if self.image and self.image.name != "default_center.jpg":
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.image.path)
        if self.pix_image and self.image.name != "default_center_pix.jpg":
            pix_img = Image.open(self.pix_image.path)
            if pix_img.height > 300 or pix_img.width > 300:
                pix_img.thumbnail((300, 300))
                pix_img.save(self.pix_image.path)

    def __str__(self):
        return f"{self.short_name} ({self.country})"

    class Meta:
        verbose_name = "center"
        verbose_name_plural = "centers"
        ordering = ["name"]
