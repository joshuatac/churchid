from django import forms
from .models import Donation, Event, Post, Announcement, PrayerRequest

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = ['donation_key', "donor", "church"]

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            "privacy": forms.Select(attrs={"class": "form-control", "placeholder": "Select privacy"}),
            "privacy_reason": forms.Select(attrs={"class": "form-control", "placeholder": "Select reason"}),
            "currency": forms.Select(attrs={"class": "form-control", "placeholder": "Select currency"}),
        }
        
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['church', 'new']
        widgets = {
            'theme': forms.TextInput(attrs={"class": "form-control"}),
            'caption': forms.TextInput(attrs={"class": "form-control"}),
            'minister': forms.TextInput(attrs={"class": "form-control"}),
            'venue': forms.TextInput(attrs={"class": "form-control"}),
            'start_at': forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            'end_at': forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
        
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['church']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'image': forms.FileInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control"}),
            'category': forms.Select(attrs={"class": "form-control"}),
        }
        
        
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        exclude = ['church']
        widgets = {
            'heading':  forms.TextInput(attrs={"class": "form-control"}),
            'content':  forms.TextInput(attrs={"class": "form-control"}),
        }
        
class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        exclude = ['church', 'sender', "new"]
        widgets = {
            'content': forms.Textarea(attrs={"class": "form-control", "placeholder":"Make your prayer request", "cols": "20", "rows": "5"}),
            'status': forms.Select(attrs={"class": "form-control py-3"}),
        }