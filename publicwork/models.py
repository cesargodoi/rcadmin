import uuid

from django.utils.translation import gettext_lazy as _
from PIL import Image
from django.conf import settings
from django.utils import timezone
from django.db import models
from rcadmin.common import (
    us_inter_char,
    short_name,
    phone_format,
    get_filename,
    GENDER_TYPES,
    LECTURE_TYPES,
    SEEKER_STATUS,
    COUNTRIES,
)


def seeker_pics(instance, filename):
    filename = get_filename(instance)
    return f"seeker_pics/{filename}"


# Temporary Registration of Seeker
class TempRegOfSeeker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("name"), max_length=80)
    birth = models.DateField(_("birth"))
    gender = models.CharField(
        _("gender"), max_length=1, choices=GENDER_TYPES, default="M"
    )
    image = models.ImageField(
        _("image"),
        default="default_profile.jpg",
        upload_to=seeker_pics,
        blank=True,
    )
    city = models.CharField(_("city"), max_length=50)
    state = models.CharField(_("state"), max_length=2)
    country = models.CharField(
        _("country"), max_length=2, choices=COUNTRIES, default="BR"
    )
    phone = models.CharField(_("phone"), max_length=20)
    email = models.EmailField()
    solicited_on = models.DateTimeField(
        _("solicited on"), default=timezone.now
    )

    def save(self, *args, **kwargs):
        self.state = str(self.state).upper()
        self.phone = phone_format(self.phone)
        super(TempRegOfSeeker, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)

    def __str__(self):
        return "{} - {} ({}-{})".format(
            self.name, self.city, self.state, self.country
        )

    class Meta:
        verbose_name = _("temporary registration of seeker")
        verbose_name_plural = _("temporary registration of seekers")


# Seeker
class Seeker(models.Model):
    center = models.ForeignKey(
        "center.Center",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("center"),
    )
    name = models.CharField(_("name"), max_length=80)
    name_sa = models.CharField(max_length=80, editable=False)
    short_name = models.CharField(
        _("short name"), max_length=40, null=True, blank=True
    )
    birth = models.DateField(_("birth"), null=True, blank=True)
    gender = models.CharField(
        _("gender"), max_length=1, choices=GENDER_TYPES, default="M"
    )
    image = models.ImageField(
        _("image"),
        default="default_profile.jpg",
        upload_to=seeker_pics,
        blank=True,
    )
    city = models.CharField(_("city"), max_length=50, blank=True)
    state = models.CharField(_("state"), max_length=2, blank=True)
    country = models.CharField(
        _("country"), max_length=2, choices=COUNTRIES, default="BR"
    )
    phone = models.CharField(_("phone"), max_length=20, blank=True)
    email = models.EmailField()
    status = models.CharField(max_length=3, choices=SEEKER_STATUS, blank=True)
    status_date = models.DateField(_("status date"), null=True, blank=True)
    observations = models.TextField(_("observations"), blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="made_by_seeker",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.name_sa = us_inter_char(self.name)
        self.short_name = short_name(self.name)
        self.state = str(self.state).upper()
        self.phone = phone_format(self.phone)
        super(Seeker, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.filename.split("/")[-1] != "default_profile.jpg":
                if img.height > 300 or img.width > 300:
                    img.thumbnail((300, 300))
                    img.save(self.image.path)

    def __str__(self):
        return "{} - {}".format(self.name, self.center)

    class Meta:
        verbose_name = _("seeker")
        verbose_name_plural = _("seekers")


# Historic of seeker
class HistoricOfSeeker(models.Model):
    seeker = models.ForeignKey(
        Seeker, on_delete=models.PROTECT, verbose_name=_("seeker")
    )
    occurrence = models.CharField(
        _("occurrence"), max_length=3, choices=SEEKER_STATUS, default="MBR"
    )
    date = models.DateField(_("date"), null=True, blank=True)
    description = models.CharField(
        _("description"), max_length=100, null=True, blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="made_by_historic_of_seeker",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"[{self.date}] {self.seeker.name} - {self.occurrence}"

    class Meta:
        verbose_name = _("historic")
        verbose_name_plural = _("historics")


# Lecture
class Lecture(models.Model):
    center = models.ForeignKey(
        "center.Center",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("center"),
    )
    type = models.CharField(
        _("type"), max_length=3, choices=LECTURE_TYPES, default="CTT"
    )
    theme = models.CharField(_("theme"), max_length=100)
    date = models.DateField(_("date"), null=True, blank=True)
    description = models.CharField(
        _("description"), max_length=200, null=True, blank=True
    )
    listeners = models.ManyToManyField(
        Seeker, through="Listener", blank=True, verbose_name=_("listeners")
    )
    is_active = models.BooleanField(_("active"), default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_lecture",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.theme} [{self.type}] - {self.center} ({self.date})"

    class Meta:
        verbose_name = _("lecture")
        verbose_name_plural = _("lectures")
        ordering = ["date"]


#  Listener
class Listener(models.Model):
    lecture = models.ForeignKey(
        Lecture, on_delete=models.PROTECT, verbose_name=_("lecture")
    )
    seeker = models.ForeignKey(
        Seeker, on_delete=models.PROTECT, verbose_name=_("seeker")
    )
    observations = models.CharField(
        _("observations"), max_length=100, null=True, blank=True
    )

    def __str__(self):
        return f"{self.lecture} - {self.seeker}"

    class Meta:
        verbose_name = _("listener")
        verbose_name_plural = _("listeners")


#  PublicworkGroup
class PublicworkGroup(models.Model):
    name = models.CharField(_("name"), max_length=50)
    center = models.ForeignKey(
        "center.Center", on_delete=models.PROTECT, verbose_name=_("center")
    )
    description = models.CharField(
        _("description"), max_length=200, null=True, blank=True
    )
    mentors = models.ManyToManyField(
        "person.Person", blank=True, verbose_name=_("mentors")
    )
    members = models.ManyToManyField(
        Seeker, blank=True, verbose_name=_("members")
    )
    is_active = models.BooleanField(_("active"), default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="made_by_publicwork_group",
        on_delete=models.PROTECT,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} - {self.center}"

    class Meta:
        verbose_name = _("publicwork group")
        verbose_name_plural = _("publicwork groups")
