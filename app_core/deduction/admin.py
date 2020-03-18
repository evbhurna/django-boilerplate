from django.contrib import admin
from .models import Deduction, TaxEntry

# Register your models here.
admin.site.register(Deduction)
admin.site.register(TaxEntry)
