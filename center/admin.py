from django.contrib import admin
from .models import Center, Responsible


admin.site.register(Responsible)


@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_filter = ["country", "state", "center_type"]
    search_fields = ["name"]
    list_display = [
        "name",
        "phone_1",
        "phone_2",
        "email",
    ]
    readonly_fields = ("created_on", "modified_on", "made_by")
    fieldsets = [
        (
            None,
            {"fields": ["name", "short_name", "center_type", "conf_center"]},
        ),
        (
            "Contact Informations",
            {"fields": ["phone_1", "phone_2", "email"]},
        ),
        (
            "Address Informations",
            {
                "fields": [
                    "address",
                    "number",
                    "complement",
                    "district",
                    "city",
                    "state",
                    "country",
                    "zip_code",
                ]
            },
        ),
        (
            "Other Informations",
            {
                "fields": [
                    "image",
                    "pix_image",
                    "pix_key",
                    "observations",
                ]
            },
        ),
        (
            "Extra modules",
            {
                "fields": [
                    "mentoring",
                    "treasury",
                    "publicwork",
                    "accommodation",
                ]
            },
        ),
        (
            "Auth Informations",
            {"fields": ["is_active", "created_on", "modified_on", "made_by"]},
        ),
    ]

    def save_model(self, request, obj, form, change):
        obj.made_by = request.user
        super().save_model(request, obj, form, change)
