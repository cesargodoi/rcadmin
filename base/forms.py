from django import forms
from center.models import Center


class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ["conf_center"]
