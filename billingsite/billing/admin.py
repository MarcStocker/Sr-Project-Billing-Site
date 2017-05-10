from django.contrib import admin
from .models import Lease, Roommate, UtilityBill, UtilityType, BillPayment, UserPayment, PaymentRequest, UserSettings

# Register your models here.
admin.site.register(Lease)
admin.site.register(Roommate)
admin.site.register(UtilityType)
admin.site.register(UtilityBill)
admin.site.register(BillPayment)
admin.site.register(UserPayment)
admin.site.register(PaymentRequest)
admin.site.register(UserSettings)
