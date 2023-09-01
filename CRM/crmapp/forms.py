from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from .models import Record
from django.utils.translation import gettext_lazy as _
class RegisterNewUser(BaseUserCreationForm):
    password1 = forms.CharField(max_length=30, min_length=8,required=True, widget= forms.TextInput(attrs={
        'class': 'form-control',
        'type' : "password",
        "name" : "password1",
        'placeholder': "Password"
    }))
    password2 = forms.CharField(max_length=30, min_length=8,required=True, widget= forms.TextInput(attrs={
        'class': 'form-control',
        'type' : "password",
        "name": "password2",
        'placeholder' : "Confirm Your Password"
    }))
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            "username": _("Username"),
            "password1": _("Password"),
            "password2": _("Confirm Password")
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "required" : True})
        self.fields["email"].widget.attrs.update({"class": "form-control","required" : True})
        self.fields["first_name"].widget.attrs.update({"class": "form-control","required" : True})
        self.fields["last_name"].widget.attrs.update({"class": "form-control","required" : True})
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm Password"
        # self.fields["password1"].help_text = "Your password must be 8-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji."

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password Don't Match")
        return password2
    def save(self, commit=True):
        user = super().save()
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AddRecord(forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'
        exclude = ['created_at', 'last_update']
        # labels = {
        #     "username": _("Username"),
        #     "first_name": _("First Name"),
        #     "last_name": _("Last Name"),
        #     "email": _("Email"),
        #     # "password1": _("Password"),
        #     # "password2": _("Confirm Password")
        # }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "required": True, "type": "text", "name": "username", "placeholder":"Username"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "required": True, "type": "text", "name": "first_name","placeholder":"First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "required": True, "type": "text", "name": "last_name","placeholder":"Last Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "required": True, "type": "email", "name": "email","placeholder":"Email"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "required": True, "type": "password", "name": "password1", "placeholder": "Password", "minlength": 8}),
            # "password2": forms.PasswordInput(attrs={"class": "form-control", "required": True, "type": "text", "name": "password2", "placeholder": "Confirm Your Password", "minlength": 8}),
        }
        help_texts = {
            "username": _("Your username must be 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
            # "password1": _("Your password must be 8-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji."),

        }
        # error_messages = {
        #     "username": _("Your username must be 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        #     "email": _("Enter a valid email address."),
        #     "password2": _("Password Don't Match"),
        # }


