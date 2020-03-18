from django.contrib import admin
from .models import Attendance, EmployeeAttendance

# Register your models here.
admin.site.register(Attendance)
admin.site.register(EmployeeAttendance)
