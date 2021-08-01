from django import forms

from .models import Workgroup, Membership
from event.models import Frequency
from schooladmin.common import HIDDEN_AUTH_FIELDS


class WorkgroupForm(forms.ModelForm):
    class Meta:
        model = Workgroup
        fields = "__all__"
        exclude = ["members"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
        widgets.update(HIDDEN_AUTH_FIELDS)


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = "__all__"
        widgets = {
            "person": forms.HiddenInput(),
            "workgroup": forms.HiddenInput(),
            "observations": forms.Textarea(attrs={"rows": 2}),
        }


class MentoringFrequencyForm(forms.ModelForm):
    class Meta:
        model = Frequency
        fields = ["ranking", "observations"]
        widgets = {
            "ranking": forms.widgets.NumberInput(attrs={"min": 0, "max": 2}),
            "observations": forms.Textarea(attrs={"rows": 2}),
        }
