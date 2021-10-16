from django import forms
from .models import Breakout_stock

class DateInput(forms.DateInput):
    input_type = 'date'

class PNFForm(forms.Form):
    date = forms.DateField(
        widget = forms.widgets.DateInput(
                    attrs={
                    'type': 'date'
                    }
                    )
        )
    