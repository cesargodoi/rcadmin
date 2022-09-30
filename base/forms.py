from django import forms
from django.utils.translation import gettext_lazy as _
from center.models import Center


class CenterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CenterForm, self).__init__(*args, **kwargs)
        self.fields["conf_center"].required = True
        self.fields["conf_center"].label = _("Center")

    class Meta:
        model = Center
        fields = ["conf_center"]
