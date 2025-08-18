from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from expense.models import DailyExpense
from income.models import Income
from datetime import date
from django.db.models import Sum
import io, base64
import matplotlib.pyplot as plt
from budget.models import Monthly_budget


def get_chart():
    """Return base64 string of current Matplotlib figure."""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    chart = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return chart

month_mapping = {
    "January": 1, "February": 2, "March": 3,
    "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9,
    "October": 10, "November": 11, "December": 12
}
def convert_month_to_number(month):
    return month_mapping.get(month)

@login_required(login_url='login')
def home(request):
    today = date.today() 
    this_month = today.month   
    if request.method == 'POST':
        year = request.POST.get('year')    
        month = request.POST.get('month') 
        month =  convert_month_to_number(month)
    else:      
        year, month = today.year, today.month

    # ====== Monthly Totals ======
    month_expense = DailyExpense.objects.filter(date__year=year, date__month=month).aggregate(total=Sum('amount'))['total'] or 0
    month_income = Income.objects.filter(date__year=year, date__month=month).aggregate(total=Sum('amount'))['total'] or 0

    # ====== Bar Chart: Expense by Category ======
    expenses = DailyExpense.objects.filter(date__year=year, date__month=month) \
                                   .values('expense_type') \
                                   .annotate(total=Sum('amount'))

    plt.switch_backend('AGG')
    plt.figure(figsize=(6, 4))
    plt.bar([e['expense_type'] for e in expenses], [float(e['total']) for e in expenses], color='skyblue')
    plt.title('Monthly Expense by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    bar_chart = get_chart()

    # ====== Pie Chart: Income by Source ======
    incomes = Income.objects.filter(date__year=year, date__month=month) \
                             .values('source') \
                             .annotate(total=Sum('amount'))

    plt.figure(figsize=(6, 4))
    plt.pie([i['total'] for i in incomes], labels=[i['source'] for i in incomes],
            autopct='%1.1f%%', startangle=90)
    plt.title(f"Income by Source in {today.strftime('%B')}")
    pie_chart = get_chart()

    # ====== Line Chart: Income vs Expense (12 Months) ======
    months_all = list(range(1, 13))
    income_list = [0] * 12
    expense_list = [0] * 12

    income_data = Income.objects.filter(date__year=year) \
                                .values('date__month') \
                                .annotate(total=Sum('amount'))

    expense_data = DailyExpense.objects.filter(date__year=year) \
                                       .values('date__month') \
                                       .annotate(total=Sum('amount'))

    for entry in income_data:
        income_list[entry['date__month'] - 1] = float(entry['total'])
    for entry in expense_data:
        expense_list[entry['date__month'] - 1] = float(entry['total'])

    plt.figure(figsize=(8, 4))
    plt.plot(months_all, income_list, marker='o', color='red', label='Income')
    plt.plot(months_all, expense_list, marker='o', color='green', label='Expense')
    plt.xticks(months_all, ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.title('Income vs Expense by Month')
    plt.legend()
    plt.tight_layout()
    line_chart = get_chart()

    check_budget_setted = Monthly_budget.objects.get(month = this_month)

    # ====== Context ======
    return render(request, 'dashboard/dashboard.html', {
        'month_expense': month_expense,
        'month_income': month_income,
        'balance':month_income - month_expense,
        'bar_chart': bar_chart,
        'pie_chart': pie_chart,
        'line_chart': line_chart,  
        'if_budget':check_budget_setted,
    })
