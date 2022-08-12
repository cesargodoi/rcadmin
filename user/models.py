from PIL import Image
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from rcadmin.common import (
    phone_format,
    get_filename,
    GENDER_TYPES,
    COUNTRIES,
)


class UserManager(BaseUserManager):
    def _create_user(
        self, email, password, is_staff, is_superuser, **extra_fields
    ):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _("email address"),
        max_length=255,
        unique=True,
        help_text=_("Enter a valid email.  <<REQUIRED>>"),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. \
                    Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


def profile_pics(instance, filename):
    filename = get_filename(instance, field="social_name")
    return f"profile_pics/{filename}"


# Profile
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("user")
    )
    social_name = models.CharField(_("social name"), max_length=80)
    gender = models.CharField(
        _("gender"), max_length=1, choices=GENDER_TYPES, default="M"
    )
    image = models.ImageField(
        _("image"), default="default_profile.jpg", upload_to=profile_pics
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
    phone = models.CharField(_("phone"), max_length=20, blank=True)
    sos_contact = models.CharField(
        _("emergency contact"), max_length=50, blank=True
    )
    sos_phone = models.CharField(
        _("emergency phone"), max_length=20, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.social_name:
            self.social_name = (
                f"<<{self.user.email.split('@')[0]}>> REQUIRES ADJUSTMENTS"
            )
        self.phone = phone_format(self.phone)
        self.sos_phone = phone_format(self.sos_phone)
        self.state = str(self.state).upper()
        super(Profile, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.filename.split("/")[-1] != "default_profile.jpg":
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)

    def __str__(self):
        return f"{self.social_name} ({self.user})"

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
