from django import forms
from crispy_forms.helper import FormHelper
from .models import PayTypes, Payment, BankFlags, FormOfPayment
from rcadmin.common import ORDER_STATUS


class PayTypeForm(forms.ModelForm):
    class Meta:
        model = PayTypes
        fields = "__all__"


class PaymentOfEvent(forms.Select):
    def create_option(self, name, value, *args, **kwargs):
        option = super().create_option(name, value, *args, **kwargs)
        if value:
            icon = self.choices.queryset.get(pk=value)  # get icon instance
            option["attrs"]["title"] = icon.title  # set option attribute
        return option


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
        widgets = {
            "ref_month": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "value": forms.widgets.NumberInput(
                attrs={
                    "placeholder": "0.00",
                    "list": "suggestedValues",
                }
            ),
        }

    def __init__(self, user=None, **kwargs):
        super(PaymentForm, self).__init__(**kwargs)
        self.fields["paytype"].queryset = PayTypes.objects.filter(
            is_active=True
        )

    field_order = ["paytype", "event", "person", "ref_month", "value", "obs"]


class BankFlagForm(forms.ModelForm):
    class Meta:
        model = BankFlags
        fields = "__all__"


class FormOfPaymentForm(forms.ModelForm):
    class Meta:
        model = FormOfPayment
        fields = "__all__"

    def __init__(self, user=None, **kwargs):
        super(FormOfPaymentForm, self).__init__(**kwargs)
        self.fields["bank_flag"].queryset = BankFlags.objects.filter(
            is_active=True
        )


class FormUpdateStatus(forms.Form):
    status = forms.ChoiceField(choices=ORDER_STATUS)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
