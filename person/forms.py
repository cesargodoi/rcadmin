from django import forms
from rcadmin.common import HIDDEN_AUTH_FIELDS
from user.models import Profile, User

from .models import Historic, Person


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["gender", "city", "state", "country"]


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["name", "birth", "is_active", "made_by", "observations"]
        widgets = {
            "observations": forms.Textarea(attrs={"rows": 2}),
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }
        widgets.update(HIDDEN_AUTH_FIELDS)


class HistoricForm(forms.ModelForm):
    class Meta:
        model = Historic
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
            "date": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "person": forms.HiddenInput(),
            "made_by": forms.HiddenInput(),
        }


# partial forms - BASIC
class BasicFormPerson(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
        exclude = ["user", "aspect", "aspect_date", "status", "observations"]
        widgets = {
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }
        widgets.update(HIDDEN_AUTH_FIELDS)


class BasicFormProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["social_name", "phone_1", "phone_2"]


# partial forms - OTHERS
class OthersFormPerson(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["observations"]
        widgets = {"observations": forms.Textarea(attrs={"rows": 2})}


class OthersFormProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "gender",
            "profession",
            "marital_status",
            "sos_contact",
            "sos_phone",
        ]


# partial forms - ADDRESS
class AddressFormProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "address",
            "number",
            "complement",
            "district",
            "city",
            "state",
            "country",
            "zip_code",
        ]


# partial forms - IMAGE
class ImageFormProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
