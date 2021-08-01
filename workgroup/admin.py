from django.contrib import admin

from .models import (
    Membership,
    Workgroup,
)


@admin.register(Workgroup)
class WorkgroupAdmin(admin.ModelAdmin):
    # list_filter = []
    list_display = [
        "name",
        "center",
        "workgroup_type",
        "aspect",
    ]
    readonly_fields = ("created_on", "modified_on", "made_by")
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "center",
                    "workgroup_type",
                    "aspect",
                    "description",
                ]
            },
        ),
        (
            "Auth Informations",
            {
                "fields": [
                    "is_active",
                    "created_on",
                    "modified_on",
                    "made_by",
                ]
            },
        ),
    ]

    def save_model(self, request, obj, form, change):
        obj.made_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = [
        "workgroup",
        "person",
        "role_type",
    ]
