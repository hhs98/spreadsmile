from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Event, MoneyDonatorInfo, Organization


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['cover', 'event_title', 'description', 'goal']


class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Organization Name'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class OrganizationForm(forms.ModelForm):
    orgcontact = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Contact Number'}))
    orglicense = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter License Number'}))
    orgaddress = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Address Number'}))

    class Meta:
        model = Organization
        fields = ['orgcontact', 'orgaddress', 'orglicense']


class MoneyDonatorForm(forms.ModelForm):
    amount = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': 'Enter Amount'}))
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Name'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    contact = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Contact'}))
    opinion = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Enter Your Opinion'}))

    class Meta:
        model = MoneyDonatorInfo
        fields = ['amount', 'name', 'email', 'contact', 'opinion']
