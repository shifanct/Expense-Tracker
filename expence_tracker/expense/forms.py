from django import forms
from . models import DailyExpense
import datetime


class DailyExpenseForm(forms.ModelForm):
    class Meta:
        model = DailyExpense
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date',
                                           'value': datetime.date.today().strftime('%Y-%m-%d')}),
        }
