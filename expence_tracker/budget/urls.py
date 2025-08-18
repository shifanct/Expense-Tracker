from django.urls import path
from . import views 


urlpatterns = [
    path('set-budget/', views.set_budget, name='set_budget'),
    path('update-budget/', views.update_budget, name='update_budget'),

]