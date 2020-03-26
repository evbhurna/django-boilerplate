from django.urls import path
from . import views

urlpatterns = [
    path('generate_payroll/', views.generatePayroll),
    path('payroll_history/', views.payrollHistory),
    path('salary_history/', views.salaryHistory)
]