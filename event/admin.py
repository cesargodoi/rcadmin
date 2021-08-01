from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Activity, Event, Frequency

admin.site.register(Activity)
admin.site.register(Frequency)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # actions
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            ngettext(
                "%d event was successfully marked as 'inactive'.",
                "%d events were successfully marked as 'inactives'.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            ngettext(
                "%d event was successfully marked as 'active'.",
                "%d events were successfully marked as 'actives'.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    make_inactive.short_description = "Mark selected events as 'inactive'."
    make_active.short_description = "Mark selected events as 'active'."

    actions = [make_inactive, make_active]

    list_display = [
        "date",
        "center",
        "activity",
        "end_date",
        "deadline",
        "status",
    ]
    readonly_fields = ("created_on", "modified_on", "made_by")
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "activity",
                    "center",
                    "date",
                    "end_date",
                    "deadline",
                    "status",
                    "description",
                    "qr_code",
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
