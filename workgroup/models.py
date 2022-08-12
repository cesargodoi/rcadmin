from django.db import models
from django.conf import settings

from django.utils.translation import gettext_lazy as _
from person.models import Person
from rcadmin.common import ASPECTS, ROLE_TYPES, WORKGROUP_TYPES


#  Workgroup
class Workgroup(models.Model):
    name = models.CharField(_("name"), max_length=50)
    center = models.ForeignKey(
        "center.Center", on_delete=models.PROTECT, verbose_name=_("center")
    )
    workgroup_type = models.CharField(
        _("type"), max_length=3, choices=WORKGROUP_TYPES
    )
    description = models.CharField(
        _("description"), max_length=200, null=True, blank=True
    )
    aspect = models.CharField(max_length=2, choices=ASPECTS, default="--")
    members = models.ManyToManyField(
        Person, through="Membership", verbose_name=_("members")
    )
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="made_by_workgroup",
        on_delete=models.PROTECT,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} - {self.center}"

    class Meta:
        verbose_name = _("workgroup")
        verbose_name_plural = _("workgroups")


#  Membership
class Membership(models.Model):
    workgroup = models.ForeignKey(
        Workgroup, on_delete=models.PROTECT, verbose_name=_("workgroup")
    )
    person = models.ForeignKey(
        Person, on_delete=models.PROTECT, verbose_name=_("person")
    )
    role_type = models.CharField(
        _("role"), max_length=3, choices=ROLE_TYPES, default="MBR"
    )
    observations = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.workgroup} - {self.person} [{self.role_type}]"

    class Meta:
        verbose_name = _("membership")
        verbose_name_plural = _("memberships")
