from django import forms

class QuotationFilterForm(forms.Form):
    start_date = forms.DateField(label='Fecha Creación', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
