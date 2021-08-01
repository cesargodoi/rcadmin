from django import forms
from schooladmin.common import HIDDEN_AUTH_FIELDS
from user.models import Profile, User

from .models import Historic, Person


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
        exclude = ["user", "aspect", "aspect_date", "status"]
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
