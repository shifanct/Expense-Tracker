from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expense.models import DailyExpense
from datetime import date
from django.db.models import Sum
from income.models import Income
import io
import base64
from matplotlib import pyplot as plt


@login_required(login_url='login')
def home(request):
    today = date.today()
    year = today.year
    month = today.month

    this_month_total_expense = DailyExpense.objects.filter(
        date__year=year, date__month=month
    ).aggregate(total=Sum('amount'))['total'] or 0

    this_month_total_income = Income.objects.filter(
        date__year=year, date__month=month
    ).aggregate(total=Sum('amount'))['total'] or 0

    this_month_expense = DailyExpense.objects.filter(
        date__year=year, date__month=month
    )

    expence_dict = {}
    expense_type_list = []
    expense_amount_list = []

    for expense in this_month_expense:
        if expense.expense_type in expence_dict:
            expence_dict[expense.expense_type] += expense.amount
        else:
            expence_dict[expense.expense_type] = expense.amount

    for key, value in expence_dict.items():
        expense_type_list.append(key)
        expense_amount_list.append(float(value))

    plt.switch_backend('AGG')  
    plt.figure(figsize=(6, 4))
    plt.bar(expense_type_list, expense_amount_list, color='skyblue')
    plt.title('Monthly Expense by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.tight_layout()

    # Save the chart to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphic = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    this_month_income = Income.objects.filter(date__year=year, date__month=month).values('source').annotate(total=Sum('amount'))
    income_source = []
    income_amount = []
    for income in this_month_income:
        income_source.append(income['source'])
        income_amount.append(income['total'])

    plt.figure(figsize=(6, 6))
    plt.pie(income_amount,labels=income_source,autopct='%1.1f%%',startangle=90)
    plt.title(f"Income by Sourse on {today.strftime("%B")}")
    buffer_pie = io.BytesIO()
    plt.savefig(buffer_pie, format='png')
    buffer_pie.seek(0)
    pie_chart = base64.b64encode(buffer_pie.getvalue()).decode()
    buffer_pie.close()




    context = {
        'month_expense': this_month_total_expense,
        'month_income': this_month_total_income,
        'bar_chart': graphic,
        'pie_chart':pie_chart,
    }
    return render(request, 'dashboard/dashboard.html', context)
