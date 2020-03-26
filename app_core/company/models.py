from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Company(models.Model):
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    is_active = models.CharField(max_length=8, default='Active')
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return "("+str(self.code)+") "+str(self.name)

class Rate(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    is_active = models.CharField(max_length=8, default='Active')
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return str(self.name)

class RateHistory(models.Model):
    rate =  models.ForeignKey(Rate, on_delete=models.CASCADE)
    time_rate = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.IntegerField(default=0)
    taxable = models.IntegerField(default=0) #0-non tax, 1-taxable
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return str(self.rate)+" "+str(self.time_rate)

    @property
    def tax(self):
        if self.taxable == 0:
            return "Non Taxed"
        else:
            return "Taxed"

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE)
    employee_number = models.CharField(max_length=32)
    gender = models.CharField(max_length=16)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32)
    suffix = models.CharField(max_length=32, blank=True)
    contact = models.CharField(max_length=32, blank=True)
    email = models.EmailField(max_length=32, blank=True)
    address = models.CharField(max_length=128, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return str(self.last_name)+" "+str(self.suffix)+", "+str(self.first_name)+" "+str(self.middle_name)[:1]+"."

