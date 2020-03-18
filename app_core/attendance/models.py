from django.db import models
from company.models import Employee

# Create your models here.
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    type = models.CharField(max_length=16)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,)


class EmployeeAttendance(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    counted_attendance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,)



