from django import forms
from django.forms import ModelForm, DateInput, DateField, extras
from django.forms.extras.widgets import SelectDateWidget
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

import datetime
import os

from .models import Lease, Roommate
from .models import UtilityBill, UtilityType
from .models import billPayment, userPayment


class UserPaymentForm(forms.ModelForm):
    date = forms.DateField(
        label="Date Due",
        help_text="Billing Due Date",
        widget=DateInput()
    )
    class Meta:
        model = userPayment
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
            'statementDate','dueDate','datepaid',
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





class addNewBillPaymentForm(forms.ModelForm):
    date = forms.DateField(
        label="Date Paid",
        help_text="Date the bill was paid on",
        widget=DateInput()
    )
    class Meta:
        model = billPayment
        fields= [
            'payer','amount','date','payType','UtilBill',
        ]

class addNewUserPaymentForm(forms.ModelForm):
    date = forms.DateField(
        label="Date Paid",
        help_text="Date that money was transferred",
        widget=DateInput()
    )
    class Meta:
        model = userPayment
        fields= [
            'payer','payee','amount','date','payType',
        ]

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
    class Meta:
        model = Roommate
        fields= [
            'name', 'house', 'user',
        ]

class sendEmailForm(forms.Form):
    textbody = forms.CharField(label='Your name', max_length=500)
