from django.contrib import admin
from .models import Payroll, PayrollEntry
# Register your models here.

admin.site.register(Payroll)
admin.site.register(PayrollEntry)
