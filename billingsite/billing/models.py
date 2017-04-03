from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail

from datetime import datetime
import smtplib
import time

sendemails   = True
sendmailtrue = True

url = "http://bills.dynu.net/utilities/"

def bill_directory_path(instance, filename):
    billname = str(instance.utilType.name.replace(' ','_'))
    print("\n\n\n\n Billname: " + billname)
    return "uploads/bills/str(self.statementDate.date(time_string, '%Y'))/" + billname + '/' + "lease_id_" + str(instance.house.id) + billname + (str(instance.statementDate.strftime('%Y.%m.%d')))

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
        all_bills           = UtilityBill.objects.filter(house_id=self.house.id)
        all_userPayments    = userPayment.objects.filter(house_id=self.house.id)
        all_paymentrequests = PaymentRequest.objects.filter(house_id=self.house.id)
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
        all_requests = PaymentRequest.objects.filter(requestee=self).exclude(requester=self)
        # Retrieve all payment requests
        owed=0
        for i in all_requests:
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
        all_payments = userPayment.objects.filter(house_id=self.house.id)
        all_requests = PaymentRequest.objects.filter(house_id=self.house.id)

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
    def emailuser(self, message, emailfrom):
        print("\n===================================")
        print("From: " + str(emailfrom))
        print("  To: " + str(self.user.email))
        print("\n")
        print(str(message))
        print("__________________________________________________________________~")
        print("Sending message...")
        if sendemails == True:
            myemailgeek  = "marcsageek@gmail.com"
            passwordgeek = "usmtfzbmbyudsvcr"
            print("  creating server")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            print("  Starting ttls")
            server.starttls()
            print("  Logging in")
            server.login(myemailgeek, passwordgeek)
            if sendmailtrue == True:
                server.sendmail(str(myemailgeek), str(self.user.email), str(message))
            print("  Quitting Server")
            server.quit()
            print("Message sent")
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

    filepath=""
    amount          = models.DecimalField(max_digits=6, decimal_places=2)
    dueDate         = models.DateField(null=True, blank=True)
    statementDate   = models.DateField(null=True, blank=True)
    datepaid        = models.DateField(null=True, blank=True, default="")
    billdoc         = models.FileField(default=" ", upload_to=bill_directory_path, blank=True, null=True, max_length=144)
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
    def createRequests(self):
        print("\n\nBegin createRequests()")
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
            time.sleep(.3)
            print("Creating Payment Request for: " + i.name)
            paymentReq = PaymentRequest.objects.create(
                                    date    = self.statementDate,
                                    amount  = self.amount/len(my_roommates),
                                    requester   = self.owner,
                                    requestee   = i,
                                    UtilBill    = self,
            )
            print("Before paymentReq.save()")
            time.sleep(.2)
            paymentReq.save()
            print("After paymentReq.save()")
            time.sleep(.2)
            print("Before paymentReq.email()")
            paymentReq.email()
            print("After paymentReq.email()")
            print("Request Saved...")
            print("Success!! Email has been sent to : " + i.name + " at: [" + i.user.email + "]\n")
        print("\n\nEND createRequests()")
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
    house       = models.ForeignKey(
                            'Lease', null=False,
                            blank=False, default="1",
                            on_delete=models.SET_DEFAULT,
                            db_constraint=False
                            )

    def __str__(self):
        return "ID: " + str(self.id) + " " + self.requester.name + " request payment of: $" + str(self.amount) + " From: " + self.requestee.name + "  - Bill ID: " + str(self.UtilBill.id)
    def email(self):
        subject     = "New Bill: $" + str(self.amount) + " > " + str(self.requester.name) + "\n\n\n"
                    #  Hello User!
        line1       = "Hello "+self.requestee.name+"!!\n\n"
                    #  You have a new bill payment request from 'Roommate' for PG&E.
        line2       = "You have a new bill payment request from '" + self.requester.name + "' for " + self.UtilBill.utilType.name + ".\n"
                    #  The amount requested is $##.##
        line3       = "The amount requested is $" + str(self.amount) + ".\n"
        line4       = "Click the link and sign in to view your bills (" + url + ")"
        line5       = "\n\nYou currently have an unpaid total of $" + str(self.requestee.getTotRemaining()) + "."
        line6       = "\n\n --The Roommate Homebase Team"

        message     = subject + line1 + line2 + line3 + line4 + line5 + line6
        # message     = "Hello "+self.requestee.name+"!!\nYou have a new bill payment request from '"+self.requester.name+"' for "+self.UtilBill.utilType.name+".\nYou will receive another email reminder in 2 weeks regarding this payment"
        emailfrom   = "NewBills"
        self.requestee.emailuser(message,emailfrom)
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
    house   = models.ForeignKey(
                        'Lease', null=False,
                        blank=False, default="1",
                        on_delete=models.SET_DEFAULT,
                        db_constraint=False
                        )
    def __str__(self):
        return "From: " + self.payer.name + " >> To: " + self.payee.name + " ||| $" + str(self.amount)
