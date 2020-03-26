from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.contrib.auth.models import User
from decimal import Decimal
from company.models import Employee

today = now

@login_required
def generatePayroll(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        pass
    else:
        return render(request, 'payroll/generatePayroll.html', {
            'user':user, 'today':today
        })

@login_required
def payrollHistory(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        pass
    else:
        return render(request, 'payroll/payrollHistory.html', {
            'user':user, 'today':today
        })

@login_required
def salaryHistory(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        pass
    else:
        return render(request, 'payroll/salaryHistory.html', {
            'user':user, 'today':today
        })