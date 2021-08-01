from django.contrib import admin
from .models import (
    Seeker,
    HistoricOfSeeker,
    Lecture,
    Listener,
    PublicworkGroup,
    TempRegOfSeeker,
)


admin.site.register(TempRegOfSeeker)


@admin.register(Seeker)
class SeekerAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "phone",
        "email",
        "birth",
        "gender",
    ]

    readonly_fields = ("created_on", "modified_on", "made_by")

    def save_model(self, request, obj, form, change):
        obj.made_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(HistoricOfSeeker)


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = [
        "theme",
        "type",
        "date",
    ]

    readonly_fields = ("created_on", "modified_on", "made_by")
    filter_horizontal = ("listeners",)

    def save_model(self, request, obj, form, change):
        obj.made_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Listener)


@admin.register(PublicworkGroup)
class PublicworkGroupAdmin(admin.ModelAdmin):
    list_display = [
        "center",
        "name",
    ]

    readonly_fields = ("created_on", "modified_on", "made_by")
    filter_horizontal = ("mentors", "members")

    def save_model(self, request, obj, form, change):
        obj.made_by = request.user
        super().save_model(request, obj, form, change)
