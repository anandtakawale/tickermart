from django import forms

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
    