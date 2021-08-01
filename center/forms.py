from django import forms
from schooladmin.common import HIDDEN_AUTH_FIELDS

from .models import Center


class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = "__all__"
        widgets = {
            "observations": forms.Textarea(attrs={"rows": 2}),
        }
        widgets.update(HIDDEN_AUTH_FIELDS)

        labels = {
            "center_type": "Type",
            "conf_center": "Conference Center",
        }


class SelectNewCenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ["conf_center"]

        labels = {
            "conf_center": "Select new center to pupils",
        }
