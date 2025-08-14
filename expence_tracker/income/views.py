from django.shortcuts import render, redirect
from . models import Income
from . forms import IncomeForm

# Create your views here.
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)  
            income.user = request.user        
            income.save()                     
            return redirect('home')
    else:
        form = IncomeForm()

    return render(request, 'income/add_income.html', {'frm': form})
