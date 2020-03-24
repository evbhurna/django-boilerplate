from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.contrib.auth.models import User
from decimal import Decimal
from company.models import Employee

from .models import Deduction

today = now


@login_required
def deductions(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        deduction = Deduction.objects.create(
            employee = Employee.objects.get(id=request.POST['employee']),
            name = request.POST['deduction'],
            amount = request.POST['amount'],
            date = request.POST['date'],
            notes = request.POST['notes']
        )
        messages.success(
            request, 'Deduction({}) for {} successfully created.'.format(deduction.name, deduction.employee))
        return redirect('/deductions/')
    else:
        employees = Employee.objects.filter(company=user.company)
        deductions = Deduction.objects.filter(employee__company=user.company)
        return render(request, 'deduction/deductions.html', {
            'user':user, 'deductions': deductions, 'employees':employees, 'today':today
        })

@login_required
def taxes(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        pass
    else:
        return render(request, 'deduction/taxes.html', {
            'user':user, 'today':today
        })