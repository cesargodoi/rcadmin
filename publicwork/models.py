import uuid

from PIL import Image
from django.conf import settings
from django.utils import timezone
from django.db import models
from schooladmin.common import (
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
    name = models.CharField(max_length=80)
    birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_TYPES, default="M")
    image = models.ImageField(
        default="default_profile.jpg", upload_to=seeker_pics, blank=True
    )
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=2, choices=COUNTRIES, default="BR")
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    solicited_on = models.DateTimeField(default=timezone.now)

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
        verbose_name = "temporary registration of seeker"
        verbose_name_plural = "temporary registration of seekers"


# Seeker
class Seeker(models.Model):
    center = models.ForeignKey(
        "center.Center",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=80)
    name_sa = models.CharField(max_length=80, editable=False)
    short_name = models.CharField(max_length=40, null=True, blank=True)
    birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_TYPES, default="M")
    image = models.ImageField(
        default="default_profile.jpg", upload_to=seeker_pics, blank=True
    )
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField("state", max_length=2, blank=True)
    country = models.CharField(max_length=2, choices=COUNTRIES, default="BR")
    phone = models.CharField("phone", max_length=20, blank=True)
    email = models.EmailField()
    status = models.CharField(max_length=3, choices=SEEKER_STATUS, blank=True)
    status_date = models.DateField(null=True, blank=True)
    observations = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
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
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)

    def __str__(self):
        return "{} - {}".format(self.name, self.center)

    class Meta:
        verbose_name = "seeker"
        verbose_name_plural = "seekers"


# Historic of seeker
class HistoricOfSeeker(models.Model):
    seeker = models.ForeignKey(Seeker, on_delete=models.PROTECT)
    occurrence = models.CharField(
        max_length=3, choices=SEEKER_STATUS, default="MBR"
    )
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
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
        verbose_name = "historic"
        verbose_name_plural = "historics"


# Lecture
class Lecture(models.Model):
    center = models.ForeignKey(
        "center.Center",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    type = models.CharField(max_length=3, choices=LECTURE_TYPES, default="CTT")
    theme = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    listeners = models.ManyToManyField(Seeker, through="Listener", blank=True)
    is_active = models.BooleanField(default=True)
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
        verbose_name = "lecture"
        verbose_name_plural = "lectures"
        ordering = ["date"]


#  Listener
class Listener(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.PROTECT)
    seeker = models.ForeignKey(Seeker, on_delete=models.PROTECT)
    ranking = models.IntegerField(default=0)
    observations = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.lecture} - {self.seeker} [{self.ranking}]"

    class Meta:
        verbose_name = "listener"
        verbose_name_plural = "listeners"


#  PublicworkGroup
class PublicworkGroup(models.Model):
    name = models.CharField(max_length=50)
    center = models.ForeignKey("center.Center", on_delete=models.PROTECT)
    description = models.CharField(max_length=200, null=True, blank=True)
    mentors = models.ManyToManyField("person.Person", blank=True)
    members = models.ManyToManyField(Seeker, blank=True)
    is_active = models.BooleanField(default=True)
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
        verbose_name = "publicwork group"
        verbose_name_plural = "publicwork groups"
