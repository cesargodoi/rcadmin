import uuid

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from PIL import Image
from rcadmin.common import (
    get_filename,
    phone_format,
    CENTER_TYPES,
    COUNTRIES,
    RESPOSABILITIES,
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
    name = models.CharField(_("name"), max_length=50, unique=True)
    short_name = models.CharField(
        _("short name"), max_length=25, null=True, blank=True
    )
    address = models.CharField(_("address"), max_length=50, blank=True)
    number = models.CharField(_("number"), max_length=10, blank=True)
    complement = models.CharField(_("complement"), max_length=50, blank=True)
    district = models.CharField(_("district"), max_length=50, blank=True)
    city = models.CharField(_("city"), max_length=50, blank=True)
    state = models.CharField(_("state"), max_length=2, blank=True)
    country = models.CharField(
        _("country"), max_length=2, choices=COUNTRIES, default="BR"
    )
    zip_code = models.CharField(_("zip"), max_length=15, blank=True)
    phone_1 = models.CharField(_("phone"), max_length=20, blank=True)
    phone_2 = models.CharField(_("backup phone"), max_length=20, blank=True)
    email = models.CharField(max_length=60, blank=True)
    image = models.ImageField(
        _("image"),
        default="default_center.jpg",
        upload_to=center_pics,
        blank=True,
    )
    pix_image = models.ImageField(
        _("pix image"),
        default="default_center_pix.jpg",
        upload_to=center_pix_pics,
        blank=True,
    )
    pix_key = models.CharField(
        _("pix key"), max_length=50, unique=True, null=True, blank=True
    )
    center_type = models.CharField(
        _("type"), max_length=3, choices=CENTER_TYPES, default="CNT"
    )
    conf_center = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("conference center"),
    )
    responsible_for = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Responsible",
        blank=True,
        verbose_name=_("responsible"),
    )
    observations = models.CharField(
        _("observations"), max_length=200, null=True, blank=True
    )
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
        verbose_name = _("center")
        verbose_name_plural = _("centers")
        ordering = ["name"]


#  Responsible
class Responsible(models.Model):
    center = models.ForeignKey(
        Center,
        on_delete=models.PROTECT,
        verbose_name=_("center"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("user"),
    )
    rule = models.CharField(
        _("rule"), max_length=3, choices=RESPOSABILITIES, default="BDG"
    )

    def __str__(self):
        return "center: {} user: {} rule: {}".format(
            self.center, self.user, self.rule
        )

    class Meta:
        verbose_name = _("responsible")
        verbose_name_plural = _("responsibles")
