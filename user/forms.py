from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Username'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password1 = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Password'}))
    password2 = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MoneyDonatorForm(forms.ModelForm):
    # event = forms.ChoiceField(widget=forms.Select(
    #     attrs={'selected': 'One Taka Meal'}))
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
        fields = '__all__'
