from django import forms
from users.models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name','leader']
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter department name"}),
            "leader": forms.Select(attrs={"class": "form-control", "placeholder": "Select leader"}),
        }


