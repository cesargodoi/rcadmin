from django import forms
from rcadmin.common import HIDDEN_AUTH_FIELDS

from .models import Center


class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = [
            "name",
            "center_type",
            "conf_center",
            "city",
            "state",
            "country",
            "email",
            "is_active",
            "made_by",
        ]
        widgets = {}
        widgets.update(HIDDEN_AUTH_FIELDS)

        labels = {
            "center_type": "Type",
            "conf_center": "Conference Center",
        }


# partial forms - BASIC
class BasicCenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = [
            "name",
            "short_name",
            "center_type",
            "conf_center",
            "email",
            "phone_1",
            "phone_2",
            "secretary",
            "is_active",
            "made_by",
        ]
        widgets = {}
        widgets.update(HIDDEN_AUTH_FIELDS)

        labels = {
            "center_type": "Type",
            "conf_center": "Conference Center",
        }


# partial forms - ADDRESS
class AddressCenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = [
            "address",
            "number",
            "complement",
            "district",
            "city",
            "state",
            "country",
            "zip_code",
            "made_by",
        ]
        widgets = {}
        widgets.update(HIDDEN_AUTH_FIELDS)


# partial forms - OTHERS
class OthersCenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = [
            "pix_key",
            "pix_image",
            "responsible_for",
            "observations",
            "made_by",
        ]
        widgets = {"observations": forms.Textarea(attrs={"rows": 2})}
        widgets.update(HIDDEN_AUTH_FIELDS)


# partial forms - IMAGE
class ImageCenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ["image"]


class SelectNewCenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ["conf_center"]

        labels = {
            "conf_center": "Select new center to pupils",
        }
