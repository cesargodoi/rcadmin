from django.contrib import admin
from .models import Order, PayTypes, Payment, BankFlags, FormOfPayment


# admin.site.register(Order)
admin.site.register(PayTypes)
# admin.site.register(Payment)
admin.site.register(BankFlags)
admin.site.register(FormOfPayment)


@admin.register(Payment)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "paytype",
        "value",
        "reference",
        "person",
        "event",
        "created_on",
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_filter = []
    list_display = [
        "center",
        "person",
        "amount",
        "status",
        "self_payed",
    ]
    readonly_fields = ("created_on", "modified_on", "made_by")
    filter_horizontal = ("payments", "form_of_payments")
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "center",
                    "person",
                    "self_payed",
                ]
            },
        ),
        (
            "Payables an Form of Payables",
            {
                "fields": [
                    "payments",
                    "form_of_payments",
                ]
            },
        ),
        (
            "How much",
            {
                "fields": [
                    "amount",
                    "status",
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
