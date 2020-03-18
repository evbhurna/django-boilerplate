from django.contrib import admin
from .models import Company, Employee, Rate, RateHistory

# Register your models here.
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Rate)
admin.site.register(RateHistory)
