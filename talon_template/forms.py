from django import forms
from talon.models import Talon


class TalonForm(forms.ModelForm):
    class Meta:
        model = Talon
        fields = '__all__'
        widgets = {
            'talon_number': forms.Select(choices=Talon.TALON_NUMBER_CHOICES),
            'date_received': forms.DateInput(attrs={'type': 'date'}),
            'discipline_order_date': forms.DateInput(attrs={'type': 'date'}),
        }
