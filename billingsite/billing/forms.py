from django import forms
from django.forms import ModelForm, DateInput, DateField, extras
from django.forms.extras.widgets import SelectDateWidget
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

import datetime
import os

from .models import Lease, Roommate, UserSettings
from .models import UtilityBill, UtilityType
from .models import BillPayment, UserPayment


class UserPaymentForm(forms.ModelForm):
	date = forms.DateField(
		label="Date Due",
		help_text="Billing Due Date",
		widget=DateInput()
	)
	class Meta:
		model = UserPayment
		fields= [
			'payer','payee',
			'date','amount','payType'
		]
# Adding a New utility Type
class addUtilityTypeForm(forms.ModelForm):
	name = forms.CharField()
	website = forms.CharField()
	class Meta:
		model = UtilityType
		fields= [
			'name','website',
			'serviceType', 'image'
		]
class addNewBillForm(forms.ModelForm):
	owner = forms.ModelChoiceField(
		queryset=UtilityBill.objects.all(),
		label="Owner",
		help_text="Date the bill is due by",
		widget=DateInput(),
		required=False
	)
	dueDate = forms.DateField(
		label="Date Due",
		help_text="Date the bill is due by",
		widget=DateInput()
	)
	statementDate = forms.DateField(
		label="Statement Date",
		help_text="Day Bill was issued",
		widget=DateInput()
	)
	datepaid = forms.DateField(
		label="Date Paid",
		help_text="Date the Bill was paid",
		widget=DateInput(),
		required=False,
	)
	billdoc = forms.FileField(
		label="Bill Document",
		help_text="Upload a PDF or Image of your bill",
		required=False,
	)
	class Meta:
		model = UtilityBill
		fields= [
			'utilType','amount', 'billdoc',
			'statementDate','dueDate','datepaid','owner'
		]
	def setVars(self, roommate, house, commit=True):
		thisbill = UtilityBill()
		thisbill.utilType = self.cleaned_data['utilType']
		thisbill.amount = self.cleaned_data['amount']
		thisbill.statementDate = self.cleaned_data['statementDate']
		thisbill.dueDate = self.cleaned_data['dueDate']
		if self.cleaned_data['datepaid'] != "":
			thisbill.datepaid = self.cleaned_data['datepaid']
		else:
			thisbill.datepaid = ""
		thisbill.datepaid = self.cleaned_data['datepaid']
		if self.cleaned_data['billdoc'] != "":
			thisbill.billdoc = self.cleaned_data['billdoc']
		else:
			thisbill.billdoc = null

		thisbill.house = house
		thisbill.owner = roommate
		thisbill.save()
		thisbill.createRequests()
	def specifyOwner(self, house, commit=True):
		thisbill = UtilityBill()
		thisbill.utilType = self.cleaned_data['utilType']
		thisbill.amount = self.cleaned_data['amount']
		thisbill.statementDate = self.cleaned_data['statementDate']
		thisbill.dueDate = self.cleaned_data['dueDate']
		thisbill.owner = self.cleaned_data['owner']
		if self.cleaned_data['datepaid'] != "":
			thisbill.datepaid = self.cleaned_data['datepaid']
		else:
			thisbill.datepaid = ""
		thisbill.datepaid = self.cleaned_data['datepaid']
		if self.cleaned_data['billdoc'] != "":
			thisbill.billdoc = self.cleaned_data['billdoc']
		else:
			thisbill.billdoc = null

		thisbill.house = house
		thisbill.save()
		thisbill.createRequests()
class addNewBillPaymentForm(forms.ModelForm):
	date = forms.DateField(
		label="Date Paid",
		help_text="Date the bill was paid on",
		widget=DateInput()
	)
	class Meta:
		model = BillPayment
		fields= [
			'payer','amount','date','payType','UtilBill',
		]
class addNewUserPaymentForm(forms.ModelForm):
	date = forms.DateField(
		label="Date Paid",
		help_text="Date that money was transferred",
		widget=DateInput()
	)
	payer = forms.ModelChoiceField(
		queryset=Roommate.objects.all(),
		to_field_name="",
		label="You",
		required=False
	)
	payee = forms.ModelChoiceField(
		queryset=Roommate.objects.all(),
		to_field_name="",
		label="Pay To"
	)
	house = forms.ModelChoiceField(
		queryset=Lease.objects.all(),
		required=False
	)
	class Meta:
		model = UserPayment
		fields= [
			'payee','amount','date','payType','payer', 'house'
		]
	def setPayer(self, payinguser, house):
		thisPayment = UserPayment()
		thisPayment.payee = self.cleaned_data['payee']
		thisPayment.amount = self.cleaned_data['amount']
		thisPayment.date = self.cleaned_data['date']
		thisPayment.payType = self.cleaned_data['payType']
		thisPayment.payer = Roommate.objects.get(pk=payinguser.id)
		thisPayment.house = house

		thisPayment.save()

	def setVars(self, roommate, house, commit=True):
		thisbill = UtilityBill()
		thisbill.utilType = self.cleaned_data['utilType']
		thisbill.amount = self.cleaned_data['amount']
		thisbill.statementDate = self.cleaned_data['statementDate']
		thisbill.dueDate = self.cleaned_data['dueDate']
		if self.cleaned_data['datepaid'] != "":
			thisbill.datepaid = self.cleaned_data['datepaid']
		else:
			thisbill.datepaid = ""
		thisbill.datepaid = self.cleaned_data['datepaid']
		if self.cleaned_data['billdoc'] != "":
			thisbill.billdoc = self.cleaned_data['billdoc']
		else:
			thisbill.billdoc = null

		thisbill.house = house
		thisbill.owner = roommate
		thisbill.save()
		thisbill.createRequests()
class addUtilityBillPaymentForm(forms.ModelForm):
	class Meta:
		model = UtilityBill
		fields= [

		]
class addLeaseForm(forms.ModelForm):
	startDate = forms.DateField(
		label="Lease Start Date",
		help_text="The day the lease begins",
		widget=DateInput()
	)
	endDate = forms.DateField(
		label="Lease End Date",
		help_text="The day the lease ends",
		widget=DateInput()
	)
	class Meta:
		model = Lease
		fields= [
			'name', 'address', 'startDate', 'endDate',
		]
class addRoommateForm(forms.ModelForm):
	# roommatename = forms.CharField(
	# 	label="What would you like your public name to be?",
	# 	help_text="Name your roommates will see",
	# )
	class Meta:
		model = Roommate
		fields= [
			'name', 'house', 'user',
		]
class sendEmailForm(forms.Form):
	textbody = forms.CharField(label='Your name', max_length=500)
class editUserSettingsGLOBAL(forms.ModelForm):
	class Meta:
		model = UserSettings
		fields = [
			# 'venmoAcct', 'phonenumber', 'googleWallet', 'paypal'
			'venmoAcct', 'phonenumber'
		]
