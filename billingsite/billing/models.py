from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import F, FloatField, Sum

from datetime import datetime, date
import smtplib
import time, os

sendemails   = True
sendmailtrue = False

url = "http://homebase.dynu.net/utilities/"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def bill_directory_path(instance, filename):
	billname = str(instance.utilType.name.replace(' ','_'))
	filetype = filename[-4:]
	path = "uploads/bills/"
	fileformat = str(instance.statementDate.strftime('%Y'))+ "/" + billname + '/' + "lease_id_" + str(instance.house.id) + '_' + billname + '_' + (str(instance.statementDate.strftime('%Y.%m.%d'))) + (str(filetype))
	print("Filetype: " + filetype)
	print("\n\n\n\n Billname: " + billname)
	print("---\nSaving File to Location:\n"+path+fileformat)
	return os.path.join(path, fileformat)

# Create your models here.
class Lease(models.Model):
	class Meta:
		ordering=('id', 'name')
	name        = models.CharField(max_length=50)
	address     = models.CharField(max_length=50)
	startDate   = models.DateField(null=True, blank=True)
	endDate     = models.DateField(null=True, blank=True)

	def __str__(self):
		return "#" + str(self.id) + " - " + str(self.name)
class UserSettings(models.Model):
	class Meta:
		ordering=('id', 'user')
	user        = models.OneToOneField(
						User, null=False,
						blank=False, default="",
						on_delete=models.CASCADE,
						db_constraint=False
						)
	venmoAcct 	= models.CharField(
						max_length=20,
						null=True,
						blank=True,
						default=""
						)
	phonenumber = models.CharField(
						max_length=10,
						null=True,
						blank=True,
						default=""
						)
	def __str__(self):
		return "#" + str(self.id) + " - " + self.user


class Roommate(models.Model):
	class Meta:
		ordering=('id', 'name')
	user        = models.OneToOneField(
						User, null=False,
						blank=False, default="",
						on_delete=models.SET_DEFAULT,
						db_constraint=False
						)
	name        = models.CharField(max_length=25)
	house       = models.ForeignKey(
						'Lease', null=False,
						blank=False, default="",
						on_delete=models.SET_DEFAULT,
						db_constraint=False
						)
	## isactive    = models.BooleanField(default=True)
	## utiltotalowed       = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
	## utiltotalpaid       = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
	## utilpercentowed     = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
	## utiltotalowed       = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
	## utiltotaldebt       = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
	## utiltotalpaid       = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
	## utiltotalremaining  = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
##
	## ioutotalowed        = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
	## ioutotalpaid        = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
	## ioutotalowed        = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
	## ioutotaldebt        = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
	## ioutotalpaid        = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)
	## ioutotalremaining   = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True, blank=True)


	def __str__(self):
		return "#" + str(self.id) + " - " + str(self.name)
	def getPercentPaid(self):
		# print("_________ getPercentPaid() BEGIN")
		totalowed = self.getTotOwed()
		totalpaid = self.getTotPaid()
		# print("TotalOwed == " + str(totalowed))
		# print("TotalPaid == " + str(totalpaid))
		if totalowed == 0 or str(totalowed) == "None":
			# print("All Paid Up")
			# print("\n ____\n END")
			return 100
		elif totalpaid == 0 or str(totalpaid) == "None":
			# print("Nothing Paid yet")
			# print("\n ____\n END")
			return 0
		else:
			percentowed = totalowed - totalpaid
			percentowed = percentowed / totalowed
			percentowed = percentowed - 1
			percentowed = percentowed * -1
			percentowed = round(percentowed*100,2)
			# print("Percent Paid= " + str(percentowed) + "%")
			# print("\n ____\n END")
			return percentowed
	def getOwedTo(self, rmid):
		owed = PaymentRequest.objects.filter(payer_id=self.id).aggregate(Sum(F('amount'))).get('amount__sum', 0.00)
		if str(owed) == "None":
			return 0
		else:
			return owed
	def getTotOwed(self):
		owed = PaymentRequest.objects.filter(requestee=self).exclude(requester=self).aggregate(Sum(F('amount'))).get('amount__sum', 0.00)
		if str(owed) == "None":
			return 0
		else:
			return owed
	def getTotDebt(self):
		# Retrieve all payment requests
		owed=self.getTotOwed()
		# Retrieve all Payments made
		paid=self.getTotPaid()
		totDebt = owed - paid
		# print("Total Debt for '" + self.name + "' :"+ str(totDebt))
		return totDebt
	def getTotPaid(self):
		paid = UserPayment.objects.filter(payer=self).exclude(payee=self).aggregate(Sum(F('amount'))).get('amount__sum', 0.00)
		if str(paid) == "None":
			return 0
		else:
			return paid

	def iouGetOwedTo(self, owedto):
		return 0


	def getTotRemaining(self):
		debt=self.getTotDebt()
		paid=self.getTotPaid()
		print("Printing Total Left...")
		print("debt = " + str(debt))
		print("paid = " + str(paid))
		leftover=debt+paid
		print("Leftover = " + str(leftover))
		return leftover
	def getTotCollections(self):
		all_payments = UserPayment.objects.all()
		all_requests = PaymentRequest.objects.all()

		# Retrieve all Requests owed to cur user
		collections = round(0, 2)
		for i in all_requests:
			if i.requester == self and i.requestee != self:
				collections+=round(i.amount, 2)

		# Retrieve all Payments made to cur user
		paid = round(0, 2)
		for i in all_payments:
			if i.payee == self:
				paid+=round(i.amount, 2)

		totcollections = collections - paid
		return int(round(totcollections,2))
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
	image       = models.FileField(max_length=144, upload_to='utilityImgs', null=True, blank=True)

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
	billdoc         = models.FileField(default=" ", upload_to=bill_directory_path ,max_length=144, null=True, blank=True)
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
	description		= models.TextField(null=True, blank=True)

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
			print("Creating Payment Request for: " + i.name)
			paymentReq = PaymentRequest.objects.create(
									date    = self.statementDate,
									amount  = self.amount/len(my_roommates),
									requester   = self.owner,
									requestee   = i,
									UtilBill    = self,
			)
			print("Before paymentReq.save()")
			paymentReq.save()
			print("After paymentReq.save()")
			print("Before paymentReq.email()")
			paymentReq.email()
			print("After paymentReq.email()")
			print("Request Saved...")
			print("Success!! Email has been sent to : " + i.name + " at: [" + i.user.email + "]\n")
		print("\n\nEND createRequests()")
	def mysave(self, user, house, *args, **kwargs):
		self.owner = user
		self.house = house
		super(UtilityBill, self).save(*args, **kwargs)
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
		line0       = "New Bill: $" + str(self.amount) + " > " + str(self.requester.name) + "\n\n\n"
		line1       = "New Bill: $" + str(round(self.amount,2)) + " > " + str(self.requester.name) + "\n\n\n"
		line2       = "Hello "+self.requestee.name+"!!\n\n"
					#  You have a new bill payment request from 'Roommate' for PG&E.
		line3       = "You have a new bill payment request from '" + self.requester.name + "' for " + self.UtilBill.utilType.name + ".\n"
					#  The amount requested is $##.##
		line4       = "The amount requested is $" + str(round(self.amount,2)) + ".\n"
		line5       = "Click the link and sign in to view your bills (" + url + ")"
		line6       = "\n\nYou currently have an unpaid total of $" + str(self.requestee.getTotRemaining()) + "."
		line7       = "\n\n --The Roommate Homebase Team"

		message     = line0 + line1 + line2 + line3 + line4 + line5 + line6 + line7
		# message     = "Hello "+self.requestee.name+"!!\nYou have a new bill payment request from '"+self.requester.name+"' for "+self.UtilBill.utilType.name+".\nYou will receive another email reminder in 2 weeks regarding this payment"
		emailfrom   = "NewBills"
		self.requestee.emailuser(message,emailfrom)
class BillPayment(models.Model):
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
class UserPayment(models.Model):
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
