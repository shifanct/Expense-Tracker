from django.urls import path
from . import views

urlpatterns = [
    path('add_income/',views.add_income, name = 'add_income')
]