from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

import datetime

# Create your models here.
class Lease(models.Model):
    class Meta:
        ordering=('id', 'name')
    name        = models.CharField(max_length=15)
    address     = models.CharField(max_length=50)
    startDate   = models.DateField(null=True, blank=True)
    endDate     = models.DateField(null=True, blank=True)

    def __str__(self):
        return "#" + str(self.id) + " - " + str(self.name)

class Roommate(models.Model):
    class Meta:
        ordering=('id', 'name')
    name        = models.CharField(max_length=25)
    house       = models.ForeignKey(
                        'Lease', null=False,
                        blank=False, default="",
                        on_delete=models.SET_DEFAULT,
                        db_constraint=False
                        )
    user        = models.ForeignKey(
                        User, null=False,
                        blank=False, default="",
                        on_delete=models.SET_DEFAULT,
                        db_constraint=False
                        )
    isactive    = models.BooleanField(default=True)
    totalowed   = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    totalpaid   = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    percentowed = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return "#" + str(self.id) + " - " + str(self.name)

    def getPercentOwed(self):
        print("\n ~~~~ \n getPercentOwed()")
        all_bills        = UtilityBill.objects.all()
        all_userPayments = userPayment.objects.all()
        all_paymentrequests = PaymentRequest.objects.all()
        totalowed=0
        totalpaid=0
        for i in all_paymentrequests:
            if i.requestee.id == self.id:
                totalowed += i.amount
        print("Total owed=",totalowed)
        for i in all_userPayments:
            if i.payer.id == self.id:
                totalpaid+=i.amount
        print("Total paid=",totalpaid)
        percentowed = totalpaid - totalowed
        print("\n ____\n END")
        if totalowed == 0:
            return 100
        elif totalpaid == 0:
            return 0
        else:
            percentowed = percentowed / totalowed
            percentowed = round(percentowed*100,2)
            return percentowed

    def getOwedTo(self, rmid):
        owed = 0
        for i in PaymentRequest.objects.all():
            if i.payer.id == self.id:
                if i.requester.id == rmid:
                    owed+=i.amount
        return owed

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
    image           = models.FileField(max_length=144, upload_to='uploads/%Y/%m%d/', null=True, blank=True, default="")
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
        return "#" + str(self.id) + "-" + str(self.utilType.name) + "  $" + str(self.amount) + "  due by: " + str(self.dueDate)
    def createRequests(self, roommates):
        print("\n ~~~~ \n createRequests()")
        return 0


class PaymentRequest(models.Model):
    class Meta:
        ordering =('id', 'date')
    date        = models.DateField()
    amount      = models.DecimalField(max_digits=6, decimal_places=2)
    requester   = models.ForeignKey(
                            'Roommate', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False, related_name="requester"
                            )
    requestee       = models.ForeignKey(
                            'Roommate', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False, related_name="requestee"
                            )
    UtilBill    = models.ForeignKey(
                            'UtilityBill', null=False,
                            blank=False, default="",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False
                            )

class billPayment(models.Model):
    class Meta:
        ordering =('id', 'date')
    date        = models.DateField()
    amount      = models.DecimalField(max_digits=6, decimal_places=2)
    payType     = models.CharField(max_length=25)
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
    payType = models.CharField(max_length=25)
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
