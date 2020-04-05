from company.models import Employee, Rate, RateHistory
from deduction.models import Deduction, TaxEntry
from attendance.models import Attendance
from decimal import Decimal
from datetime import timedelta
import datetime
from calendar import monthrange

from deduction.helpers import sssContribution, pagIbigContribution, philhealthContribution, monthlyTax2020


def getGrossPay(employee, start_date, end_date):
    total_attendance = Attendance.objects.filter(
        employee=employee,
        time_in__gte=start_date,
        time_in__lte=datetime.datetime.strptime(
            end_date, "%Y-%m-%d") + datetime.timedelta(days=1)
    )

    total_work_time = 0.00
    for item in total_attendance:
        total_work_time = Decimal(total_work_time) + Decimal(item.work_time)

    rate = RateHistory.objects.filter(
        rate=employee.rate).order_by('-last_modified')[0]
    if rate.rate.period == 0:
        gross_pay = rate.time_rate * Decimal(total_work_time) / Decimal(480.00)
    else:
        working_days = getWorkingDays(start_date, end_date)
        gross_pay = rate.time_rate * \
            (Decimal(total_work_time) / Decimal(480.00)) / Decimal(working_days)
    return {'gross_pay': gross_pay, 'attendance': Decimal(total_work_time) / Decimal(480.00)}


def getTotalDeduction(employee, start_date, end_date):
    total_deduction = Deduction.objects.filter(
        employee=employee,
        date__gte=start_date,
        date__lte=end_date
    )

    total_deduction_amount = Decimal(0.00)
    for item in total_deduction:
        total_deduction_amount = total_deduction_amount + item.amount

    return Decimal(total_deduction_amount)


def getNetPayroll(request, start_date, end_date):
    user = Employee.objects.get(user=request.user)
    employees_list = Employee.objects.filter(company=user.company)
    salary_list = []
    for employee in employees_list:
        rate = RateHistory.objects.filter(rate=employee.rate).order_by('-last_modified')[0]
        gross_pay = getGrossPay(employee, start_date, end_date)
        total_deductions = getTotalDeduction(employee, start_date, end_date)
        taxable_pay = gross_pay['gross_pay'] - total_deductions
        tax = Decimal(monthlyTax2020(taxable_pay))
        net_pay = taxable_pay - tax

        if gross_pay['attendance'] > 0:
            salary_list.append(
                {
                    'employee': employee,
                    'attendance': gross_pay['attendance'],
                    'rate': rate,
                    'gross_pay': gross_pay['gross_pay'],
                    'total_deductions': Decimal(total_deductions),
                    'taxable_pay': taxable_pay,
                    'tax': tax,
                    'net_pay': net_pay
                }
            )
        else:
            pass

    return salary_list

def getEmployeeNetPayroll(employee, start_date, end_date):
    salary = {}

    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    rate = RateHistory.objects.filter(rate=employee.rate).order_by('-last_modified')[0]
    gross_pay = getGrossPay(employee, start_date, end_date)
    total_deductions = getTotalDeduction(employee, start_date, end_date)
    taxable_pay = gross_pay['gross_pay'] - total_deductions
    tax = Decimal(monthlyTax2020(taxable_pay))
    net_pay = taxable_pay - tax

    if gross_pay['attendance'] > 0:
        salary['employee']= employee
        salary['attendance']= gross_pay['attendance']
        salary['rate']= rate
        salary['gross_pay']= gross_pay['gross_pay']
        salary['total_deductions']= Decimal(total_deductions)
        salary['taxable_pay']= taxable_pay
        salary['tax']= tax
        salary['net_pay']= net_pay
    else:
        pass

    return salary

def getWorkingDays(start_date, end_date):
    w_days = 0
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    month = start_date.month
    year = start_date.year

    last_date = monthrange(year, month)[1]
    for i in range(1, last_date+1):
        try:
            thisdate = datetime.date(year, month, i)
        except(ValueError):
            break
        if thisdate.weekday() < 5:
            w_days = w_days + 1

    return w_days


def auto_sss(employee, start_date, end_date):
    if check_deduction_exists(employee, start_date, 'SSS'):
        pass
    else:
        if employee.auto_sss == 1:
            if employee.rate.period == 1:
                rate = RateHistory.objects.filter(
                    rate=employee.rate).order_by('-last_modified')[0].time_rate
            else:
                rate = RateHistory.objects.filter(
                    rate=employee.rate).order_by('-last_modified')[0].time_rate
                rate = 23 * rate
            contribution = sssContribution(rate)
            deduction = Deduction.objects.create(
                employee=employee,
                auto='AUTO',
                date=start_date,
                name='Contribution',
                notes='SSS',
                amount=contribution['EE']+contribution['EC']
            )
        else:
            pass


def auto_philhealth(employee, start_date, end_date):
    if check_deduction_exists(employee, start_date, 'Philhealth'):
        pass
    else:
        if employee.auto_philhealth == 1:
            if employee.rate.period == 1:
                rate = RateHistory.objects.filter(
                    rate=employee.rate).order_by('-last_modified')[0].time_rate
            else:
                rate = RateHistory.objects.filter(
                    rate=employee.rate).order_by('-last_modified')[0].time_rate
                rate = 23 * rate
            contribution = philhealthContribution(rate)
            deduction = Deduction.objects.create(
                employee=employee,
                auto='AUTO',
                date=start_date,
                name='Contribution',
                notes='Philhealth',
                amount=contribution
            )
        else:
            pass


def auto_pagibig(employee, start_date, end_date):
    if check_deduction_exists(employee, start_date, 'Pag Ibig'):
        pass
    else:
        if employee.auto_pagibig == 1:
            if employee.rate.period == 1:
                rate = RateHistory.objects.filter(
                    rate=employee.rate).order_by('-last_modified')[0].time_rate
            else:
                rate = RateHistory.objects.filter(
                    rate=employee.rate).order_by('-last_modified')[0].time_rate
                rate = 23 * rate
            contribution = pagIbigContribution(rate)
            deduction = Deduction.objects.create(
                employee=employee,
                auto='AUTO',
                date=start_date,
                name='Contribution',
                notes='Pag Ibig',
                amount=contribution
            )
        else:
            pass


def auto_tax(employee, start_date, end_date):
    if employee.auto_tax == 1:
        if employee.rate.period == 1:
            rate = RateHistory.objects.filter(
                rate=employee.rate).order_by('-last_modified')[0].time_rate
        else:
            rate = RateHistory.objects.filter(
                rate=employee.rate).order_by('-last_modified')[0].time_rate
            rate = 23 * rate # 23 days is arbitrary working days per month to compute a monthly rate from daily rate
        contribution = auto_pagibig(rate)
        deduction = Deduction.objects.create(
            employee=employee,
            auto='AUTO',
            date=start_date,
            name='Contribution',
            notes='Pag Ibig',
            amount=contribution
        )
    else:
        pass


def create_deductions(request, start_date, end_date):
    user = Employee.objects.get(user=request.user)
    employees_list = Employee.objects.filter(company=user.company)
    for employee in employees_list:
        auto_sss(employee, start_date, end_date)
        auto_philhealth(employee, start_date, end_date)
        auto_pagibig(employee, start_date, end_date)

def check_deduction_exists(employee, start_date, notes):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    if Deduction.objects.filter(
        employee=employee, 
        date__month=start_date.month, 
        date__year=start_date.year,
        auto='AUTO',
        notes=notes):
        return True
    else:
        return False

def get_deductions(employee, start_date, end_date):
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    deductions = Deduction.objects.filter(
        employee=employee,
        date__gte=start_date,
        date__lte=end_date
    )

    return deductions
