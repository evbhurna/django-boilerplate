from company.models import Employee, Rate, RateHistory
from deduction.models import Deduction, TaxEntry
from attendance.models import Attendance
from decimal import Decimal

def getGrossPay(employee, start_date, end_date):
    total_attendance = Attendance.objects.filter(
        employee = employee,
        time_in__gte = start_date,
        time_in__lte = end_date
    )

    total_work_time = 0.00
    for item in total_attendance:
        total_work_time = Decimal(total_work_time) + Decimal(item.work_time)

    rate = RateHistory.objects.filter(rate=employee.rate).reverse()[0]
    
    gross_pay = rate.time_rate * Decimal(total_work_time) / Decimal(480.00)
    return gross_pay

def getTotalDeduction(employee, start_date, end_date):
    total_deduction = Deduction.objects.filter(
        employee = employee,
        date__gte = start_date,
        date__lte = end_date
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
        gross_pay = getGrossPay(employee, start_date, end_date)
        total_deductions = getTotalDeduction(employee, start_date, end_date)
        net_pay = gross_pay -  total_deductions

        salary_list.append(
            {
                'employee': employee,
                'gross_pay': gross_pay,
                'total_deductions': Decimal(total_deductions),
                'net_pay': net_pay
            }
        )
    
    return salary_list


