from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.contrib.auth.models import User
from decimal import Decimal
from company.models import Employee
import openpyxl
from .models import Deduction, TaxEntry

today = now


@login_required
def deductions(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        employee_list = request.POST.getlist('employee')
        for i in range(len(employee_list)):
            deduction = Deduction.objects.create(
                employee = Employee.objects.get(id=employee_list[i]),
                name = request.POST['deduction'],
                amount = request.POST['amount'],
                date = request.POST['date'],
                notes = request.POST['notes']
            )
        messages.success(
            request, 'Deduction/s successfully created.')
        return redirect('/deductions/')
    else:
        employees = Employee.objects.filter(company=user.company)
        deductions = Deduction.objects.filter(employee__company=user.company).order_by('id')[:100]
        return render(request, 'deduction/deductions.html', {
            'user':user, 'deductions': deductions, 'employees':employees, 'today':today
        })

@login_required
def deductionsUpload(request):
    user = Employee.objects.get(user=request.user)
    if request.FILES['deduction_file']:
        deduction_file = request.FILES['deduction_file']
        wb = openpyxl.load_workbook(deduction_file)
        worksheet = wb["Sheet1"]
        excel_data = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
        from django.utils.dateparse import parse_datetime
        for i in range(len(excel_data)-1):
            j = i + 1
            employee = Employee.objects.get(
                employee_number = excel_data[j][1],
                last_name__iexact = excel_data[j][0]
            ) 
            deduction = Deduction.objects.create(
                employee = employee,
                name = excel_data[j][2],
                amount = excel_data[j][5],
                date = parse_datetime(excel_data[j][4]).date(),
                notes = excel_data[j][3]
            )
        
        messages.success(
            request, 'Deduction/s file successfully uploaded.')
        return redirect('/deductions/')
    else:
        pass


@login_required
def taxes(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        pass
    else:
        return render(request, 'deduction/taxes.html', {
            'user':user, 'today':today
        })

@login_required
def myTaxes(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        pass
    else:
        taxes = Deduction.objects.filter(name='Taxes', employee=user)
        return render(request, 'deduction/myTaxes.html', {
            'user':user, 'today':today, 'taxes':taxes
        })

@login_required
def myDeductions(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        pass
    else:
        deductions = Deduction.objects.filter(employee=user)
        return render(request, 'deduction/myDeductions.html', {
            'user':user, 'today':today
        })