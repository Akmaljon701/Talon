from django import forms
from .models import Talon


class TalonForm(forms.ModelForm):
    class Meta:
        model = Talon
        fields = '__all__'
