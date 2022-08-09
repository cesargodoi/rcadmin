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


# partial forms
class ProfileFormUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user", "image"]


class PupilFormUpdate(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
        exclude = [
            "user",
            "status",
            "aspect",
            "aspect_date",
            "is_active",
            "made_by",
        ]
        widgets = {
            "observations": forms.Textarea(attrs={"rows": 3}),
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }


# partial forms - IMAGE
class ImageFormUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
