from django.db import models
from company.models import Employee
from django.utils.timezone import now
from payroll.models import PayrollEntry

class Deduction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    name = models.CharField(max_length=32)
    notes = models.TextField()
    date = models.DateField(default=now)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,)

class TaxEntry(models.Model):
    payroll_entry = models.ForeignKey(PayrollEntry, on_delete=models.CASCADE)
    tax_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    taxed_salary = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    notes = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,)

