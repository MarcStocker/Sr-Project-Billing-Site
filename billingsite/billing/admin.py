from django.contrib import admin
from .models import Lease, Roommate, UtilityBill, UtilityType, billPayment, userPayment

# Register your models here.
admin.site.register(Lease)
admin.site.register(Roommate)
admin.site.register(UtilityType)
admin.site.register(UtilityBill)
admin.site.register(billPayment)
admin.site.register(userPayment)
