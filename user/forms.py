from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MoneyDonatorForm(forms.ModelForm):
    class Meta:
        model = MoneyDonatorInfo
        fields = '__all__'
