import math
from decimal import Decimal

def sssContribution(monthly_rate):
    EC = 10 if monthly_rate < 14750 else 30
    EE = 80

    if monthly_rate >= 19750:
        EE = 800
    elif monthly_rate < 2250:
        EE = 80
    else:
        EE = 80 + 20*math.ceil((monthly_rate-2250)/500)

    ER = EE * 2

    contribution = {
        'EE':EE,
        'ER':ER,
        'EC':EC
    }

    return contribution

def pagIbigContribution(monthly_rate):
    contribution = Decimal(monthly_rate)*Decimal(0.02)

    return contribution

def philhealthContribution(monthly_rate):
    contribution = 150.00

    if monthly_rate<=10000:
        contribution = 150.00
    elif monthly_rate>40000:
        contribution = 1100.00
    else:
        contribution = Decimal(monthly_rate) * Decimal(0.015)
    
    return contribution

def monthlyTax2020(taxable_salary):
    taxable_salary = float(taxable_salary)
    if taxable_salary <= 20833:
        tax = 0.00
    elif taxable_salary > 20833 and taxable_salary < 33332:
        tax = (taxable_salary - 20833) * 0.2
    elif taxable_salary >= 33333 and taxable_salary <= 66666:
        tax = 2500 + (taxable_salary - 33333) * 0.25
    elif taxable_salary >= 66667 and taxable_salary <= 166666:
        tax = 10833.33 + (taxable_salary - 66667) * 0.30
    elif taxable_salary >= 166667 and taxable_salary <= 666666:
        tax = 40833.33 + (taxable_salary - 166667) * 0.32
    elif taxable_salary >= 666667:
        tax = 200833.33 + (taxable_salary - 666667) * 0.35
    else:
        tax = 0.00

    return tax




