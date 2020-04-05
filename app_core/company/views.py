from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.timezone import now
from django.contrib.auth.models import User
from decimal import Decimal

from .models import Employee, Rate, RateHistory

today = now


@login_required
def employees(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        middle_name = request.POST['middle_name']
        employee_number = request.POST['employee_number']

        account = User.objects.create_user(
            username=generate_username(first_name, middle_name, last_name),
            password=employee_number,
            is_staff=True,)

        employee = Employee.objects.create(
            user=account,
            company=user.company,
            rate=Rate.objects.get(id=request.POST['rate']),
            employee_number=employee_number,
            gender=request.POST['gender'],
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            suffix=request.POST['suffix'],
            contact=request.POST['contact'],
            email=request.POST['email'],
            address=request.POST['address'],)

        messages.success(
            request, '{} - Employee account successfully created.'.format(account.username))
        return redirect('/employees/')
    else:
        rates = Rate.objects.filter(is_active='Active', company=user.company)
        employees = Employee.objects.filter(company=user.company).order_by('-employee_number')
        return render(request, 'company/employees.html', {
            'user': user, 'employees': employees, 'today': today, 'rates':rates})

@login_required
def employeesView(request, id):
    user = Employee.objects.get(user=request.user)
    employee = Employee.objects.get(id=id)
    if request.method == 'POST':

        employee.rate = Rate.objects.get(id=request.POST['rate'])
        employee.employee_number = request.POST['employee_number']
        employee.gender = request.POST['gender']
        employee.first_name = request.POST['first_name']
        employee.last_name = request.POST['last_name']
        employee.middle_name = request.POST['middle_name']
        employee.suffix=request.POST['suffix']
        employee.contact=request.POST['contact']
        employee.email=request.POST['email']
        employee.address=request.POST['address']

        try:
            if request.POST['auto_sss'] == 'on':
                employee.auto_sss = 1
            else:
                employee.auto_sss = 0
        except:
            employee.auto_sss = 0
        
        try:   
            if request.POST['auto_philhealth'] == 'on':
                employee.auto_philhealth = 1
            else:
                employee.auto_philhealth = 0
        except:
            employee.auto_philhealth = 0

        try:
            if request.POST['auto_pagibig'] == 'on':
                employee.auto_pagibig = 1
            else:
                employee.auto_pagibig = 0
        except:
            employee.auto_pagibig = 0

        try:
            if request.POST['auto_tax'] == 'on':
                employee.auto_tax = 1
            else:
                employee.auto_tax = 0
        except:
            employee.auto_tax = 0

        employee.save()

        messages.success(
            request, '{} - Employee information successfully updated.'.format(employee.user.username))
        return redirect('/employees/{}/view/'.format(id))
    else:
        rates = Rate.objects.filter(company=user.company, is_active='Active')
        return render(request, 'company/employeesView.html', {
            'user': user, 'employee': employee, 'rates':rates, 'today': today})

@login_required
def rates(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        rate = Rate.objects.create(
            company=user.company, name=request.POST['name'], period=request.POST['period'])
        RateHistory.objects.create(
            rate=rate, status=1, time_rate=request.POST['time_rate'])
        messages.success(
            request, '{} - Employee rate successfully created.'.format(rate.name))
        return redirect('/rates/')
    else:
        rates = RateHistory.objects.filter(rate__company=user.company, status=1)
        return render(request, 'company/rates.html', {
            'user': user, 'rates': rates, 'today': today})

@login_required
def ratesView(request, id):
    user = Employee.objects.get(user=request.user)
    rate = Rate.objects.get(id=id)
    history = RateHistory.objects.filter(rate=rate).order_by('date_created')
    if request.method == 'POST':
        rate.name = request.POST['name']
        rate.save()

        latest_rates = RateHistory.objects.filter(rate=rate).order_by('date_created').reverse()[0]
        latest_rates.status = 0
        latest_rates.save()
        RateHistory.objects.create(
            rate=rate, time_rate=request.POST['time_rate'], status=1, taxable=request.POST['tax'])

        messages.success(
            request, '{} - Employee rate successfully updated.'.format(rate.name))
        return redirect('/rates/{}/view/'.format(id))
    else:
        latest = history.reverse()[0]
        return render(request, 'company/ratesView.html', {
            'user': user, 'latest': latest, 'today': today, 'history':history.reverse()})


def generate_username(first_name, middle_name, last_name):
    f_names = first_name.lower().split()
    f_names = [name[0] for name in f_names]
    f_names = ''.join(f_names)
    m_names = middle_name.lower().split()
    m_names = [name[0] for name in m_names]
    m_names = ''.join(m_names)
    l_names = last_name.lower().replace(' ', '')
    password = f_names + m_names + l_names
    return password

@login_required
def myProfile(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        user.gender = request.POST['gender']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.middle_name = request.POST['middle_name']
        user.suffix=request.POST['suffix']
        user.contact=request.POST['contact']
        user.email=request.POST['email']
        user.address=request.POST['address']
        user.save()

        messages.success(
            request, '{} - Employee information successfully updated.'.format(user.user.username))
        return redirect('/my_profile/')
    else:
        return render(request, 'company/myProfile.html', {
            'user': user, 'today': today})

@login_required
def changePassword(request):
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user.last_modified = now()
            user.save()
            account = form.save()
            update_session_auth_hash(request, account)  # Important!
            messages.success(request, 'Your password has been changed.')
            return redirect('/change_password/')
        else:
            pass
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'company/changePassword.html', {
        'form': form,
        'user': user
    })

@login_required
def resetPassword(request, id):
    employee = Employee.objects.get(id=id)
    user = User.objects.get(id=employee.user.id)
    user.password = employee.employee_number
    user.save()

    messages.success(request, 'Password reset successful.')
    return redirect('/employees/{}/view/'.format())

 