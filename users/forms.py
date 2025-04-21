from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Church, Member
from django.contrib.auth.password_validation import validate_password


class ChurchForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), required=True
    )

    class Meta:
        model = Church
        exclude = ["id", "is_active"]  # Removed "leader" as it's not in your model
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "disabled": True}
            ),  # Changed to EmailInput
            "denomination": forms.Select(attrs={"class": "form-control"}),
            "founded": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),  # Changed to DateInput
            "website": forms.URLInput(attrs={"class": "form-control", "type": "url"}),
            "branch_name": forms.TextInput(attrs={"class": "form-control"}),
            "branch_type": forms.Select(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "logo": forms.FileInput(attrs={"class": "form-control"}),
        }

    def clean_password(self):
        """Validate password using Django's built-in validators."""
        password = self.cleaned_data.get("password")
        validate_password(password)  # This applies Django's password validation
        return password

    def clean(self):
        """Ensure password and confirm_password match."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data





fields = [
    "first_name",
    "last_name",
    "title",
    "email",
    "address",
    "phone",
    "box_number",
    "sex",
    "department",
]

base_widgets = {
    "first_name": forms.TextInput(attrs={"class": "form-control"}),
    "last_name": forms.TextInput(attrs={"class": "form-control"}),
    "email": forms.EmailInput(attrs={"class": "form-control", "disabled": True}),
    "address": forms.TextInput(attrs={"class": "form-control"}),
    "phone": forms.TextInput(attrs={"class": "form-control"}),
    "box_number": forms.TextInput(attrs={"class": "form-control"}),
    "sex": forms.Select(attrs={"class": "form-control"}),
    "title": forms.Select(attrs={"class": "form-control"}),
    "department": forms.Select(attrs={"class": "form-control"}),
}

create_widgets = {
    **base_widgets,
    "password1": forms.PasswordInput(attrs={"class": "form-control"}),
    "password2": forms.PasswordInput(attrs={"class": "form-control"}),
}


class MemberFormCreate(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(MemberFormCreate, self).__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
    
    class Meta:
        model = Member
        fields = fields + ["password1", "password2"]
        widgets = create_widgets 


class MemberFormUpdate(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=50, required=False, widget= forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(required=False, widget= forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = Member
        fields = fields  
        widgets = base_widgets  #

