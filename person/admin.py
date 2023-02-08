from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Historic, Person, Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_filter = ["city", "state", "center", "migration", "imported"]
    search_fields = ["name", "email"]
    list_display = [
        "name",
        "id_card",
        "email",
        "center",
        "invited_on",
        "migration",
        "imported",
        "imported_on",
    ]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # actions
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            ngettext(
                "%d person was successfully marked as 'inactive'.",
                "%d persons were successfully marked as 'inactives'.",
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
                "%d person was successfully marked as 'active'.",
                "%d persons were successfully marked as 'actives'.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    make_inactive.short_description = "Mark selected persons as 'inactive'."
    make_active.short_description = "Mark selected persons as 'active'."

    actions = [make_inactive, make_active]
    list_filter = ["aspect", "status", "is_active"]
    search_fields = ["name"]
    list_display = [
        "name",
        "person_type",
        "aspect",
        "status",
    ]

    readonly_fields = ("created_on", "modified_on", "made_by")
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "user",
                    "center",
                    "reg",
                ]
            },
        ),
        (
            "Personal Informations",
            {
                "fields": [
                    "name",
                    "id_card",
                    "birth",
                ]
            },
        ),
        (
            "Pupil Informations",
            {
                "fields": [
                    "person_type",
                    "aspect",
                    "aspect_date",
                    "status",
                    "observations",
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


@admin.register(Historic)
class HistoricAdmin(admin.ModelAdmin):
    search_fields = ["person__name_sa"]
    list_filter = ["occurrence"]
    list_display = [
        "date",
        "occurrence",
        "person",
    ]
    readonly_fields = ("created_on", "modified_on", "made_by")
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "person",
                    "occurrence",
                    "date",
                    "description",
                ]
            },
        ),
        (
            "Auth Informations",
            {
                "fields": [
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
