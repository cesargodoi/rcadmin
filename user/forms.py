from django import forms

from .models import User, Profile
from treasury.models import Payment, FormOfPayment, PayTypes
from rcadmin.common import PROFILE_PAYFORM_TYPES


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class UserFormReadonly(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
        widgets = {
            "email": forms.widgets.EmailInput(attrs={"readonly": "readonly"}),
        }


class ProfileFormUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user", "image"]


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

    def __init__(self, user=None, **kwargs):
        super(MyPaymentForm, self).__init__(**kwargs)
        self.fields["paytype"].queryset = PayTypes.objects.filter(
            is_active=True
        )


class MyFormOfPaymentForm(forms.ModelForm):
    type = forms.ChoiceField(choices=PROFILE_PAYFORM_TYPES)

    class Meta:
        model = FormOfPayment
        fields = "__all__"
        exclude = ["payform_type", "complement"]


class ImageFormUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(
                attrs={"accept": "video/*;capture=camera"}
            ),
        }
