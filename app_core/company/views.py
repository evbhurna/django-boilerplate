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
        employees = Employee.objects.filter(company=user.company)
        return render(request, 'company/employees.html', {
            'user': user, 'employees': employees, 'today': today})


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
        employee.save()

        messages.success(
            request, '{} - Employee account successfully updated.'.format(employee.account.username))
        return redirect('/employees/{}/view/'.format(id))
    else:
        return render(request, 'company/employeesView.html', {
            'user': user, 'employee': employee, 'today': today})

@login_required
def rates(request):
    user = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        rate = Rate.objects.create(
            company=user.company, name=request.POST['name'])
        RateHistory.objects.create(
            rate=rate, time_rate=request.POST['time_rate'])
        messages.success(
            request, '{} - Employee rate successfully created.'.format(rate.name))
        return redirect('/rates/')
    else:
        rates = Rate.objects.filter(company=user.company)
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

        latest_rates = RateHistory.objects.filter(rate=rate).order_by('date_created')[0]
        if Decimal(request.POST['time_rate'])==Decimal(latest_rates.time_rate):
            pass
        else:
            RateHistory.objects.create(
                rate=rate, time_rate=request.POST['time_rate'])

        messages.success(
            request, '{} - Employee rate successfully updated.'.format(rate.name))
        return redirect('/rates/{}/view/'.format(id))
    else:
        return render(request, 'company/ratesView.html', {
            'user': user, 'rates': rates, 'today': today})


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
