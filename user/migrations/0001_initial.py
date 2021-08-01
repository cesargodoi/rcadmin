# Generated by Django 3.2.3 on 2021-05-19 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Enter a valid email.  <<REQUIRED>>",
                        max_length=255,
                        unique=True,
                        verbose_name="email address",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active.                     Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date joined",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("social_name", models.CharField(max_length=80)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "male"), ("F", "female")],
                        default="M",
                        max_length=1,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        default="default_profile.jpg", upload_to="profile_pics"
                    ),
                ),
                ("profession", models.CharField(blank=True, max_length=40)),
                (
                    "marital_status",
                    models.CharField(blank=True, max_length=40),
                ),
                ("address", models.CharField(blank=True, max_length=50)),
                ("number", models.CharField(blank=True, max_length=10)),
                ("complement", models.CharField(blank=True, max_length=50)),
                ("district", models.CharField(blank=True, max_length=50)),
                ("city", models.CharField(blank=True, max_length=50)),
                (
                    "state",
                    models.CharField(
                        blank=True, max_length=2, verbose_name="state"
                    ),
                ),
                ("country", models.CharField(blank=True, max_length=50)),
                (
                    "zip_code",
                    models.CharField(
                        blank=True, max_length=15, verbose_name="zip"
                    ),
                ),
                (
                    "phone_1",
                    models.CharField(
                        blank=True, max_length=15, verbose_name="phone"
                    ),
                ),
                (
                    "phone_2",
                    models.CharField(
                        blank=True, max_length=15, verbose_name="backup phone"
                    ),
                ),
                (
                    "sos_contact",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        verbose_name="emergency contact",
                    ),
                ),
                (
                    "sos_phone",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        verbose_name="emergency phone",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "profile",
                "verbose_name_plural": "profiles",
            },
        ),
    ]
