from django.shortcuts import render, redirect
from . forms import DailyExpenseForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = DailyExpenseForm(request.POST)
        if form.is_valid():
            frm = form.save(commit=False)
            frm.user = request.user
            frm.save()
            return redirect('dashboard')
        else:
            print(form.errors)
    else:    
        form = DailyExpenseForm()
    return render(request, 'expense/add_expense.html', {'form': form})