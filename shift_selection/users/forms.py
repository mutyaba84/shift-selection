# users/forms.py

from django import forms
from .models import Shift, Availability

class ShiftSelectionForm(forms.Form):
    selected_shift = forms.ModelChoiceField(queryset=Shift.objects.all(), label='Select Shift')
    selected_address = forms.CharField(max_length=100, label='Address')
    date_time_selected = forms.DateTimeField(label='Date and Time')

class ShiftOfferForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['max_users']
        labels = {
            'max_users': 'Maximum Number of Users',
        }
