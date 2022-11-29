from django import forms

# from django.utils.translation import gettext_lazy as _
from rcadmin.common import HIDDEN_AUTH_FIELDS
from user.models import Profile, User

from .models import Historic, Person, Invitation


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


class ImageFormUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


# invite person
class InvitationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.fields["birth"].required = True
        self.fields["id_card"].required = True

    class Meta:
        model = Invitation
        fields = ["name", "email", "birth", "id_card", "center"]
        widgets = {
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "email": forms.widgets.EmailInput(),
            "center": forms.HiddenInput(),
        }


#  pupil registration form  ###################################################
help_text = {
    "email": (
        "Você não pode alterar o seu email neste momento, pois ele foi \
        pré-cadastrado no sistema e é necessário para a validação deste \
        formuário.  Você poderá fazer a troca depois através da secretaria."
    ),
    "sos_contact": (
        "Indique uma pessoa de sua confiança, para que possamos entrar em \
        contato em um eventual caso de emergência envolvendo você."
    ),
}

popover = {
    "data-trigger": "hover",
    "data-container": "body",
    "data-toggle": "popover",
    "data-placement": "right",
}


class PupilRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PupilRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["birth"].required = True
        self.fields["gender"].required = True
        self.fields["id_card"].required = True
        self.fields["address"].required = True
        self.fields["number"].required = True
        self.fields["complement"].required = False
        self.fields["district"].required = True
        self.fields["city"].required = True
        self.fields["state"].required = True
        self.fields["zip_code"].required = True
        self.fields["phone"].required = True

    class Meta:
        model = Invitation
        fields = "__all__"
        exclude = ["imported"]
        widgets = {
            "birth": forms.widgets.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
            "email": forms.widgets.EmailInput(
                attrs={
                    "readonly": "readonly",
                    "title": "Importante!",
                    "data-content": help_text["email"],
                    **popover,
                }
            ),
            "sos_contact": forms.widgets.TextInput(
                attrs={
                    "title": "Porque Contato de Emergência?",
                    "data-content": help_text["sos_contact"],
                    **popover,
                }
            ),
            "sos_phone": forms.widgets.TextInput(
                attrs={
                    "title": "Porque Contato de Emergência?",
                    "data-content": help_text["sos_contact"],
                    **popover,
                }
            ),
            "center": forms.HiddenInput(),
            "invited_on": forms.HiddenInput(),
        }
