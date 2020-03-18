from django.contrib import admin
from .models import Company, Profile, Rate, RateHistory

# Register your models here.
admin.site.register(Company)
admin.site.register(Profile)
admin.site.register(Rate)
admin.site.register(RateHistory)
