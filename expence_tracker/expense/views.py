from django.shortcuts import render
from . forms import DailyExpenseForm

# Create your views here.

def add_expense(request):
    form = DailyExpenseForm
    return render(request, 'expense/add_expense.html', {'form':form})