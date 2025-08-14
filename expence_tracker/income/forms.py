from django import forms
from . models import Income
import datetime


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date',
                                           'value': datetime.date.today().strftime('%Y-%m-%d')}),
        }
        

