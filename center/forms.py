from django import forms
from rcadmin.common import HIDDEN_AUTH_FIELDS

from .models import Center, Responsible


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


# partial forms - BASIC
class InfoCenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = [
            "name",
            "center_type",
            "conf_center",
            "email",
            "phone_1",
            "phone_2",
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
        widgets = {"made_by": forms.HiddenInput()}


# partial forms - IMAGE
class ImageCenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ["image", "made_by"]
        widgets = {"made_by": forms.HiddenInput()}


# partial forms - OTHERS
class OthersCenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = [
            "short_name",
            "pix_key",
            "observations",
            "pix_image",
            "made_by",
        ]
        widgets = {
            "made_by": forms.HiddenInput(),
            "observations": forms.Textarea(attrs={"rows": 2}),
        }


class SelectNewCenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ["conf_center"]


class ResponsibleForm(forms.ModelForm):
    class Meta:
        model = Responsible
        fields = "__all__"
        widgets = {
            "center": forms.HiddenInput(),
            "user": forms.HiddenInput(),
        }
