from django.urls import path, re_path
from . import views

urlpatterns = [
    path('generate_payroll/', views.generatePayroll),
    path('payroll_history/', views.payrollHistory),
    path('salary_history/', views.salaryHistory),
    re_path(r'^generate_payroll/(?P<id>\w+)/detail/$', views.payDetails),
]