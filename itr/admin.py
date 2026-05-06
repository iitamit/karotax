from django.contrib import admin
from .models import ITRFiling, IncomeDetails, DeductionDetails
admin.site.register(ITRFiling)
admin.site.register(IncomeDetails)
admin.site.register(DeductionDetails)
