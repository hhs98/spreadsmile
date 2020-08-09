from django import forms
from django.forms import ModelForm

from .models import *


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
