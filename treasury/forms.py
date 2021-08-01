from django import forms
from crispy_forms.helper import FormHelper
from .models import PayTypes, Payment, BankFlags, FormOfPayment
from schooladmin.common import ORDER_STATUS


class PayTypeForm(forms.ModelForm):
    class Meta:
        model = PayTypes
        fields = "__all__"


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
        widgets = {
            "ref_month": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }


class BankFlagForm(forms.ModelForm):
    class Meta:
        model = BankFlags
        fields = "__all__"


class FormOfPaymentForm(forms.ModelForm):
    class Meta:
        model = FormOfPayment
        fields = "__all__"
        widgets = {
            "payform_type": forms.Select(
                attrs={"v-model": "selected", "v-on:change": "viewHide()"}
            )
        }


class FormUpdateStatus(forms.Form):
    status = forms.ChoiceField(choices=ORDER_STATUS)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
