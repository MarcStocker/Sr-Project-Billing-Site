from django.db import models
from datetime import datetime
import datetime

# Create your models here.
class Lease(models.Model):
    class Meta:
        ordering=('id', 'name')
    name        = models.CharField(max_length=15)
    address     = models.CharField(max_length=50)
    startDate   = models.DateField()
    endDate     = models.DateField()

    def __str__(self):
        return "#" + str(self.id) + " - " + str(self.name)

class Roommate(models.Model):
    class Meta:
        ordering=('id', 'name')
    name    = models.CharField(max_length=25)
    house   = models.ForeignKey(
                        'Lease', null=False,
                        blank=False, default="",
                        on_delete=models.SET_DEFAULT,
                        db_constraint=False
                        )
    # user    = models.ForeignKey()

    def __str__(self):
        return "#" + str(self.id) + " - " + str(self.name)

class UtilityType(models.Model):
    class Meta:
        ordering =('id', 'name')
    name        = models.CharField(max_length=20)
    website     = models.CharField(max_length=200)
    serviceType = models.CharField(max_length=50)
    image       = models.FileField(max_length=144, upload_to='uploads/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return "#" + str(self.id) + " - " + str(self.name)

class UtilityBill(models.Model):
    class Meta:
        ordering =('id', 'dueDate')
    amount          = models.DecimalField(max_digits=6, decimal_places=2)
    dueDate         = models.DateField(null=True, blank=True)
    statementDate   = models.DateField(null=True, blank=True)
    datepaid        = models.DateField(null=True, blank=True)
    owner           = models.ForeignKey(
                                'Roommate', null=False,
                                blank=False, default="",
                                on_delete=models.SET_DEFAULT,
                                db_constraint=False
                                )
    house           = models.ForeignKey(
                                'Lease', null=False,
                                blank=False, default="",
                                on_delete=models.SET_DEFAULT,
                                db_constraint=False
                                )
    utilType        = models.ForeignKey(
                                'UtilityType', null=False,
                                blank=False, default="",
                                on_delete=models.SET_DEFAULT,
                                db_constraint=False
                                )

    def __str__(self):
        return "#" + str(self.id) + "-" + str(self.utilType.name) + "  due: " + str(self.amount) + "  by: " + str(self.dueDate)

class billPayment(models.Model):
    class Meta:
        ordering =('id', 'date')
    date        = models.DateField()
    amount      = models.DecimalField(max_digits=6, decimal_places=2)
    payType     = models.TextField()
    payer       = models.ForeignKey(
                            'Roommate', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False
                            )
    UtilBill    = models.ForeignKey(
                            'UtilityBill', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False
                            )

class userPayment(models.Model):
    class Meta:
        ordering =('id', 'date')
    date    = models.DateField(null=True, blank=True)
    amount  = models.DecimalField(max_digits=6, decimal_places=2)
    payType = models.TextField()
    payer   = models.ForeignKey(
                        'Roommate', null=False,
                        blank=False, default="",
                        on_delete=models.SET_DEFAULT,
                        db_constraint=False, related_name="payer"
                        )
    payee   = models.ForeignKey(
                        'Roommate', null=False,
                        blank=False, default="",
                        on_delete=models.SET_DEFAULT,
                        db_constraint=False, related_name="payee"
                        )
