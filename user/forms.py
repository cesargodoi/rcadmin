from django import forms
from .models import User, Profile
from treasury.models import Payment, FormOfPayment
from rcadmin.common import PROFILE_PAYFORM_TYPES


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            "image": forms.FileInput(
                attrs={"accept": "video/*;capture=camera"}
            ),
        }


class MyPaymentForm(forms.ModelForm):
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
            "person": forms.HiddenInput(),
        }


class MyFormOfPaymentForm(forms.ModelForm):
    type = forms.ChoiceField(choices=PROFILE_PAYFORM_TYPES)

    class Meta:
        model = FormOfPayment
        fields = "__all__"
        exclude = ["payform_type", "complement"]
