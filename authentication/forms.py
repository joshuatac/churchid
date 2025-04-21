from django import forms
from .models import Otp

class LoginForm(forms.Form):
    user_id = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), required=True)


class EmailForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control"}), required=True)