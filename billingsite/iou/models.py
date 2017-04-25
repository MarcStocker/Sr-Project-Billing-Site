from django.db import models
from billing.models import Lease, Roommate

# Create your models here.
class Bill(models.Model):
    class Meta:
        ordering =('id', 'date')
    date    = models.DateField()
    amount  = models.DecimalField(max_digits=6, decimal_places=2)
    owner   = models.ForeignKey(
                            'billing.Roommate', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False
                            )
    Description = models.CharField(max_length=200)

class PaymentRequest(models.Model):
    class Meta:
        ordering =('id', 'date')
    date        = models.DateField()
    amount      = models.DecimalField(max_digits=6, decimal_places=2)
    requester   = models.ForeignKey(
                            'billing.Roommate', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False, related_name="iourequester"
                            )
    requestee   = models.ForeignKey(
                            'billing.Roommate', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False, related_name="iourequestee"
                            )
    Bill        = models.ForeignKey(
                            'Bill', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False
                            )
    house       = models.ForeignKey(
                            'billing.Lease', null=False,
                            blank=False, default="1",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False, related_name="iouhouse"
                            )

    def __str__(self):
        return "ID: " + str(self.id) + " " + self.requester.name + " request payment of: $" + str(self.amount) + " From: " + self.requestee.name + "  - Bill ID: " + str(self.UtilBill.id)
