from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expense.models import DailyExpense
from datetime import date
from django.db.models import Sum
from income.models import Income

# Create your views here.
@login_required(login_url='login')
def home(request):
    today = date.today()
    year = today.year
    month = today.month
    this_month_total_expense = DailyExpense.objects.filter(date__year = year , date__month = month).aggregate(
        total = Sum('amount'))['total']
    this_month_total_income = Income.objects.filter(date__year = year , date__month = month).aggregate(
        total = Sum('amount'))['total']
    
    context = {
        'month_expense': this_month_total_expense,
        'month_income': this_month_total_income,
    }
    return render(request, 'dashboard/dashboard.html', context)