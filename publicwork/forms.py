from django import forms
from schooladmin.common import HIDDEN_AUTH_FIELDS

from .models import (
    TempRegOfSeeker,
    Seeker,
    Lecture,
    Listener,
    HistoricOfSeeker,
    PublicworkGroup,
)


class TempRegOfSeekerForm(forms.ModelForm):
    class Meta:
        model = TempRegOfSeeker
        fields = "__all__"
        widgets = {
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }
        widgets.update({"solicited_on": forms.HiddenInput()})


class SeekerForm(forms.ModelForm):
    class Meta:
        model = Seeker
        fields = "__all__"
        widgets = {
            "observations": forms.Textarea(attrs={"rows": 2}),
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }
        widgets.update(HIDDEN_AUTH_FIELDS)


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = "__all__"
        exclude = ["listeners"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
            "date": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
        }
        widgets.update(HIDDEN_AUTH_FIELDS)


class ListenerForm(forms.ModelForm):
    class Meta:
        model = Listener
        fields = ["ranking", "observations"]
        widgets = {
            "ranking": forms.widgets.NumberInput(attrs={"min": 0, "max": 2}),
        }


class HistoricForm(forms.ModelForm):
    class Meta:
        model = HistoricOfSeeker
        exclude = ["listeners"]
        widgets = {
            "descriptions": forms.Textarea(attrs={"rows": 2}),
            "date": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "seeker": forms.HiddenInput(),
        }
        widgets.update(HIDDEN_AUTH_FIELDS)


class GroupForm(forms.ModelForm):
    class Meta:
        model = PublicworkGroup
        exclude = ["mentors", "members"]
        widgets = {
            "descriptions": forms.Textarea(attrs={"rows": 2}),
        }
        widgets.update(HIDDEN_AUTH_FIELDS)
