from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.contrib.auth.models import User
from decimal import Decimal
from company.models import Employee
from datetime import datetime

today = now

@login_required
def generatePayroll(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        date_range = request.POST['litepicker']
        start_date = date_range[:10]
        end_date = date_range[13:]

        from . import helpers
        helpers.create_deductions(request, start_date, end_date)
        payroll = helpers.getNetPayroll(request, start_date, end_date)
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        return render(request, 'payroll/generatePayroll.html', {
            'user':user, 'today':today, 'payroll':payroll,
            'start_date': start_date, 'end_date':end_date
        })
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

@login_required
def payDetails(request, id):
    user = Employee.objects.get(user=request.user)
    employee = Employee.objects.get(id=id)
    start_date = datetime.strptime(request.GET['start_date'], "%B %d, %Y")
    end_date = datetime.strptime(request.GET['end_date'], "%B %d, %Y")
    from . import helpers
    salary = helpers.getEmployeeNetPayroll(employee, start_date, end_date)
    deductions = helpers.get_deductions(employee, start_date, end_date)
    if request.method == 'POST':
        pass
    else:
        return render(request, 'payroll/payDetail.html', {
            'user':user, 'today':today, 'employee':employee,
            'start_date':start_date, 'end_date':end_date, 'salary':salary,
            'deductions':deductions
        })