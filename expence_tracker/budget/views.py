from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . models import Monthly_budget
import datetime

# Create your views here.

@login_required(login_url='login')
def set_budget(request):
    if request.method == "POST":
        month = datetime.date.today().month
        budget = request.POST.get("budget")
        user = request.user
        Monthly_budget.objects.create(user=user, budget=budget, month=month)
        return redirect('dashboard')
    

def update_budget(request):
    if request.method == 'POST':
        this_month = datetime.date.today().month
        budget = request.POST.get("budget")
        budget_obj = Monthly_budget.objects.get(user = request.user, month = this_month)
        budget_obj.budget = budget
        budget_obj.save()
        return redirect('dashboard')
        
