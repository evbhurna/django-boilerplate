from django.db import models
from django.utils.timezone import now
from company.models import Company, Employee, RateHistory

# Create your models here.
class Payroll(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,)

class PayrollEntry(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rate_recorded = models.ForeignKey(RateHistory, on_delete=models.CASCADE)
    net_amount = models.DecimalField(decimal_places=2, max_digits=10)
    total_deductions = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    total_tax = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    total_attendance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,)
    
