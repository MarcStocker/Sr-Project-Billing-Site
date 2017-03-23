from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail

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
    def getPercentPaid(self):
        # print("\n ~~~~ \n getPercentOwed()")
        # print("FOR USER: " + self.name)
        all_bills           = UtilityBill.objects.all()
        all_userPayments    = userPayment.objects.all()
        all_paymentrequests = PaymentRequest.objects.all()
        totalowed=0
        totalpaid=0
        for i in all_paymentrequests:
            if i.requestee.id == self.id and i.requester.id != i.requestee.id:
                totalowed += i.amount
        # print("Total owed=",totalowed)
        for i in all_userPayments:
            if i.payer.id == self.id:
                totalpaid+=i.amount
        # print("Total paid=",totalpaid)
        percentowed = totalowed - totalpaid
        if totalowed == 0:
            # print("All Paid Up")
            # print("\n ____\n END")
            return 100
        elif totalpaid == 0:
            # print("Nothing Paid yet")
            # print("\n ____\n END")
            return 0
        else:
            percentowed = percentowed / totalowed
            percentowed = percentowed - 1
            percentowed = percentowed * -1
            percentowed = round(percentowed*100,2)
            # print("Percent Paid= " + str(percentowed) + "%")
            # print("\n ____\n END")
            return percentowed
    def getOwedTo(self, rmid):
        owed = 0
        for i in PaymentRequest.objects.all():
            if i.payer.id == self.id:
                if i.requester.id == rmid:
                    owed+=i.amount
        return owed
    def getTotOwed(self):
        all_requests = PaymentRequest.objects.all()
        # Retrieve all payment requests
        owed=0
        for i in all_requests:
            if i.requestee == self:
                owed+=i.amount
        return owed
    def getTotDebt(self):
        # Retrieve all payment requests
        owed=self.getTotOwed()
        # Retrieve all Payments made
        paid=self.getTotPaid()
        totDebt = self.getTotOwed() - self.getTotPaid()
        # print("Total Debt for '" + self.name + "' :"+ str(totDebt))
        return totDebt
    def getTotPaid(self):
        all_payments = userPayment.objects.all()
        # Retrieve all Payments made
        paid=0
        for i in all_payments:
            if i.payer == self:
                paid+=i.amount
        return paid
    def getTotRemaining(self):
        all_payments = userPayment.objects.all()
        all_requests = PaymentRequest.objects.all()

        # Retrieve all Requests owed to cur user
        debt=self.getTotDebt()
        paid=self.getTotPaid()

        leftover=debt-paid
        return leftover
    def getTotCollections(self):
        all_payments = userPayment.objects.all()
        all_requests = PaymentRequest.objects.all()

        # Retrieve all Requests owed to cur user
        collections = 0
        for i in all_requests:
            if i.requester == self and i.requestee != self:
                collections+=i.amount

        # Retrieve all Payments made to cur user
        paid=0
        for i in all_payments:
            if i.payee == self:
                paid+=i.amount

        totcollections = collections - paid
        return totcollections
    def emailuser(self, subject, message, emailfrom):
        print("\n===================================================================")
        print("   Emailing User: New Bill Created")
        print("Sending Email To: " + self.user.email)
        print("            From: " + emailfrom)
        print("Subject: "+ subject)
        print("---------------------------------------- ")
        print(message)
        # send_mail(str(subject), str(message), str(emailfrom)+'@RoommateHomebase.com', [str(self.user.email)], fail_silently=False)
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
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
    datepaid        = models.DateField(null=True, blank=True, default="")
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

    def save(self, *args, **kwargs):
        super(UtilityBill, self).save(*args, **kwargs)

    def createRequests(self):
        # print("\n ~~~~ \n createRequests()")
        all_roommates = Roommate.objects.all()
        my_roommates  = []
        # print("--- Roommate in House ---")
        for i in all_roommates:
            if i.house.id == self.house.id:
                # print("Roomie: " + i.name)
                my_roommates.append(i)

        print("----")

        # Create a new PaymentRequest for each Roommate
        for i in my_roommates:
            print("Creating Payment Request for: " + i.name)
            paymentReq = PaymentRequest.objects.create(
                                    date    = self.statementDate,
                                    amount  = self.amount/len(my_roommates),
                                    requester   = self.owner,
                                    requestee   = i,
                                    UtilBill    = self,
            )
            paymentReq.save()
            print("Success!!\n")
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
    requestee   = models.ForeignKey(
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

    def __str__(self):
        return self.requester.name + " request payment of: $" + str(self.amount) + " From: " + self.requestee.name
    def save(self, *args, **kwargs):
        subject     = "New Bill: $" + str(self.amount) + " > " + self.requester.name
                    #  Hello User!
        line1       = "Hello "+self.requestee.name+"!!\n"
                    #  You have a new bill payment request from 'Roommate' for PG&E.
        line2       = "You have a new bill payment request from '" + self.requester.name + "' for " + self.UtilBill.utilType.name + ".\n"
                    #  The amount requested is $##.##
        line3       = "The amount requested is $" + str(self.amount) + "."
                    #  You will receive another reminder in 2 weeks.
        message     = "Hello "+self.requestee.name+"!!\nYou have a new bill payment request from '"+self.requester.name+"' for "+self.UtilBill.utilType.name+".\nYou will receive another email reminder in 2 weeks regarding this payment"
        emailfrom   = "NewBills"
        self.requestee.emailuser(subject,message,emailfrom)
        super(PaymentRequest, self).save(*args, **kwargs)
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
    def __str__(self):
        return self.payer.name + " " + self.UtilBill.utilType.name + " - $" + str(self.amount) + " || Payed on: " + str(self.date)
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
    def __str__(self):
        return "From: " + self.payer.name + " >> To: " + self.payee.name + " ||| $" + str(self.amount)
