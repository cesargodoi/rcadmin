from django import forms

from .models import Activity, Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ["frequencies"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
            "date": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "end_date": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "deadline": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "datetime-local"}
            ),
            "is_active": forms.HiddenInput(),
            "made_by": forms.HiddenInput(),
        }


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = "__all__"


class FrequenciesAddForm(forms.Form):
    frequencies = forms.CharField(widget=forms.Textarea(attrs={"rows": 6}))
