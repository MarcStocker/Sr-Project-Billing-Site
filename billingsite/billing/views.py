from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F, FloatField, Sum

from .models import PaymentRequest, UserSettings
from .models import Lease, Roommate, UtilityBill
from .models import UtilityType, BillPayment, UserPayment
from .forms import addLeaseForm, addRoommateForm
from .forms import addUtilityBillPaymentForm, addNewBillForm
from .forms import addNewBillPaymentForm, addNewUserPaymentForm
from .forms import UserPaymentForm, addUtilityTypeForm, sendEmailForm

from decimal import *


from datetime import datetime, date
import random
import os
import time
import smtplib

# Create your views here.
@login_required(login_url="/login/")

def billinghome(request):
	if not Roommate.objects.filter(user_id=request.user.id):
		print("User is not associated with a house")
		context = { 'page_name':"Join a House"}
		return render(request, 'billing/joincreatehouse.html', context)

	print("\n\n\n\n==========================================================")
	print("def billinghome(request)")
	print(">>>>>>>>>>>>>>>>>>>\n\n")


	cur_roommate = Roommate.objects.get(user=request.user.id)
	house        = cur_roommate.house
	my_roommates = Roommate.objects.filter(house_id=house.id).order_by('id')

	# WIP:0 - Debt Tab
	roommates_iowe       = {}
	roommate_collections = {}
	for i in my_roommates:
		if i.id != cur_roommate.id:
			# Code for Roommates_iowe
			all_requests = PaymentRequest.objects.filter(requester_id=i.id, requestee_id=cur_roommate.id)
			userpayments = UserPayment.objects.filter(payee_id=i.id, payer_id=cur_roommate.id)
			temptotbill = 0
			temptotpay   = 0
			for bill in all_requests:
				temptotbill+=bill.amount
			for payment in userpayments:
				temptotpay+=payment.amount
			temptotstillowed = temptotbill - temptotpay
			if temptotstillowed >= 1:
				roommates_iowe[i.name] = [temptotbill, temptotpay, temptotstillowed]
			elif temptotstillowed <0:
				roommate_collections[i.name] = [temptotbill, temptotpay, temptotstillowed]

			# Code for Roommate_Collections
			all_requests = PaymentRequest.objects.filter(requester_id=cur_roommate.id, requestee_id=i.id)
			userpayments = UserPayment.objects.filter(payee_id=cur_roommate.id, payer_id=i.id)
			temptotpayments     = 0
			temptotcollections  = 0
			for charge in all_requests:
				temptotcollections += charge.amount
			for payment in userpayments:
				temptotpayments += payment.amount
			temptotstillowed=temptotcollections-temptotpayments
			print("Total Still Owed: " + str(temptotstillowed))
			if temptotstillowed >= 1:
				roommate_collections[i.name] = [temptotcollections, temptotpayments, temptotstillowed]





	# DONE - Total Collections of Current User
	curuser_collect= PaymentRequest.objects.filter(requester=cur_roommate).exclude(requestee=cur_roommate).aggregate(Sum(F('amount'))).get('amount__sum', 0.00)
	curuser_collected= UserPayment.objects.filter(payee=cur_roommate).exclude(payer=cur_roommate).aggregate(Sum(F('amount'))).get('amount__sum', 0.00)
	print("curuser_collect:")
	print(curuser_collect)
	print("curuser_collected:")
	print(curuser_collected)
	if str(curuser_collect) == "None":
		curuser_collect = 0
	if str(curuser_collected) == "None":
		curuser_collected = 0
	curuser_collect -= curuser_collected
	# DONE - Total Debt Of Current User
	curuser_debt = PaymentRequest.objects.filter(requestee=cur_roommate).exclude(requester=cur_roommate).aggregate(Sum(F('amount'))).get('amount__sum', 0.00)
	if str(curuser_debt) == "None":
		curuser_debt = 0
	curuser_payments= UserPayment.objects.filter(payer=cur_roommate).exclude(payee=cur_roommate).aggregate(Sum(F('amount'))).get('amount__sum', 0.00)
	if str(curuser_payments) == "None":
		curuser_payments = 0
	curuser_debt = curuser_payments - curuser_debt
	totmoney = curuser_collect - -curuser_debt
	# TODO:60 - Display all Bill by month in new Tab
	# TODO:70 - Display all Payments for each user in a new Tab

	numroommates= 0

	roommateowes=[]
	roommatepaid=[]

	# TODO:50 - All Bills Associated With House
	all_bills = UtilityBill.objects.filter(house_id=house.id)
	all_bills = all_bills.order_by('-dueDate')
	last5bills= all_bills.order_by('-dueDate')[:5]

	#
	all_payments    = UserPayment.objects.filter(house_id=house.id)

	print("\n-------------------\n      END \n-------------------\n END BILLING HOME \n-------------------\n\n")
	context = {
		'page_name'         :"Utilities - Roommate Homebase",
		'house'             :house,
		'totmoney'          :totmoney,
		'all_bills'         :all_bills,
		'last5bills'        :last5bills,
		'curuser_debt'      :curuser_debt,
		'all_payments'      :all_payments,
		'numroommates'      :numroommates,
		'roommateowes'      :roommateowes,
		'roommatepaid'      :roommatepaid,
		'my_roommates'      :my_roommates,
		'roommates_iowe'    :roommates_iowe,
		'curuser_collect'   :curuser_collect,
		'roommate_collections':roommate_collections,
	}
	return render(request, 'billing/billinghome.html', context)
@login_required(login_url="/login/")
def addbill(request):
	cur_roommate = Roommate.objects.get(user=request.user.id)
	house        = cur_roommate.house
	my_roommates = Roommate.objects.filter(house_id=house.id)
	if request.method=='POST':
		form = addNewBillForm(request.POST, request.FILES)
		if form.is_valid():
			# if request.user.is_superuser == True:
				# form.specifyOwner(house)
			# else:
			form.setVars(cur_roommate, house)

			return HttpResponseRedirect('/utilities/')
	else:
		form = addNewBillForm()
	context = {
		'page_name' :"Add New Bill - Roommate Homebase",
		'sitename'  :"Roommate Homebase",
		'page_name' :"Add a Bill",
		'form':form,
	}
	return render(request, 'billing/addBill.html', context)
@login_required(login_url="/login/")
def addbilltype(request):
	if request.method=='POST':
		form = addUtilityTypeForm(request.POST)
		if form.is_valid():
			j = form.save(request, commit=False)
			j.save()
			return HttpResponseRedirect('/utilities/')
	else:
		form = addNewBillForm()
	context = {
		'page_name' :"Add a New Bill Type - Roommate Homebase",
		'sitename'  :"Roommate Homebase",
		'page_name' :"Add a Bill Payment",
		'form'      :form,
	}
	return render(request, 'billing/addBill.html', context)
@login_required(login_url="/login/")
def addbillpayment(request):
	if request.method=='POST':
		form = addNewBillPaymentForm(request.POST, request.FILES)
		if form.is_valid():
			j = form.save(request)
			j.save()
			return HttpResponseRedirect('/utilities/')
	else:
		form = addNewBillPaymentForm()
	context = {
		'page_name' :"Add Bill Payment - Roommate Homebase",
		'sitename'  :"Roommate Homebase",
		'page_name' :"Add a Bill Payment",
		'form'      :form,
	}
	return render(request, 'billing/addBillPayment.html', context)
@login_required(login_url="/login/")
def adduserpayment(request):
	if request.method=='POST':
		form = addNewUserPaymentForm(request.POST)
		if form.is_valid():
			cur_roommate = Roommate.objects.get(user=request.user.id)
			house        = cur_roommate.house
			form.setPayer(cur_roommate, house )
			return HttpResponseRedirect('/utilities/')
		else:
			return HttpResponseRedirect('/utilities/addUserPayment/')
	else:
		# print(datetime.today().strfttime("%m/%d/%Y"))
		thedate = "Todays Date: {:%m/%d/%Y}".format(datetime.now())
		cur_roommate = Roommate.objects.get(user=request.user.id)
		house        = cur_roommate.house
		my_roommates = Roommate.objects.filter(house_id=house.id).order_by('id')
		form = addNewUserPaymentForm()
		form.fields['payee'].queryset = my_roommates
		form.date = thedate
		usersettings = {}
		for i in my_roommates:
			usersettings[i.id] = UserSettings.objects.get(user=i.user).venmoAcct
		roommates_iowe       = {}
		for i in my_roommates:
			if i.id != cur_roommate.id:
				# Code for Roommates_iowe
				all_requests = PaymentRequest.objects.filter(requester_id=i.id, requestee_id=cur_roommate.id)
				userpayments = UserPayment.objects.filter(payee_id=i.id, payer_id=cur_roommate.id)
				temptotbill = 0
				temptotpay   = 0
				for bill in all_requests:
					temptotbill+=bill.amount
				for payment in userpayments:
					temptotpay+=payment.amount
				temptotstillowed = temptotbill - temptotpay
				if temptotstillowed >= 1:
					roommates_iowe[i.name] = [temptotbill, temptotpay, temptotstillowed]
		context = {
			'page_name'     :"Add User Payment - Roommate Homebase",
			'sitename'      :"Roommate Homebase",
			'page_name'     :"Add a User Payment",
			'my_roommates'  :my_roommates,
			'roommates_iowe':roommates_iowe ,
			'usersettings'	:usersettings,
			'form'          :form,
		}
	return render(request, 'billing/addUserPayment.html', context)
	# return render(request, 'billing/testing.html', context)
# @login_required(login_url="/login/")
# def venmopayment(request, user_id):

@login_required(login_url="/login/")
def addlease(request):
	if request.method=='POST':
		form = addLeaseForm(request.POST)
		if form.is_valid():
			j = form.save(request)
			j.save()
			print("Successfully Created Lease: " + j.name)
			newRoommate = Roommate()
			newRoommate.house= j
			newRoommate.user = request.user
			newRoommate.name = request.user.username
			newRoommate.save()
			return HttpResponseRedirect('/utilities/')
	else:
		form = addLeaseForm()
	context = {
		'page_name' :"Add Lease - Roommate Homebase",
		'sitename'  :"Roommate Homebase",
		'page_name' :"Add a Lease",
		'form'      :form,
	}
	return render(request, 'billing/addLease.html', context)
@login_required(login_url="/login/")
def addroommate(request):
	if request.method=='POST':
		form = addRoommateForm(request.POST)
		if form.is_valid():
			j = form.save(request)
			j.save()
			return HttpResponseRedirect('/utilities/')
	else:
		form = addRoommateForm()
	context = {
		'page_name'     :"Add Roommate - Roommate Homebase",
		'sitename'      :"Roommate Homebase",
		'form'          :form,
	}
	return render(request, 'billing/addRoommate.html', context)
@login_required(login_url="/login/")
def addself(request):
	if request.method=='POST':
		form = addRoommateForm(request.POST)
		form.user = request.user
		print("User to be added: " + request.user)
		if form.is_valid():
			#j = form.save(request)
			#j.save()
			return HttpResponseRedirect('/utilities/')
	else:
		form = addRoommateForm()
	context = {
		'page_name'     :"Add Roommate - Roommate Homebase",
		'sitename'      :"Roommate Homebase",
		'form'          :form,
	}
	return render(request, 'billing/addSelf.html', context)
@login_required(login_url="/login/")
def admintablepage(request):
	all_users           = User.objects.all()
	all_leases          = Lease.objects.all()
	all_roommates       = Roommate.objects.all()
	all_userpayments    = UserPayment.objects.all()
	all_billpayments    = BillPayment.objects.all()
	all_utilityBills    = UtilityBill.objects.all()
	all_utilityTypes    = UtilityType.objects.all()
	all_PaymentRequests = PaymentRequest.objects.all()

	context = {
		'sitename'  :"Roommate Homebase",
		'page_name' :"Admin - All Tables",
		'all_users'          :all_users,
		'all_leases'         :all_leases,
		'all_roommates'      :all_roommates,
		'all_userpayments'   :all_userpayments,
		'all_billpayments'   :all_billpayments,
		'all_utilityBills'   :all_utilityBills,
		'all_utilityTypes'   :all_utilityTypes,
		'all_PaymentRequests':all_PaymentRequests,
	}
	return render(request, 'billingsite/adminTablePage.html', context)
@login_required(login_url="/login/")
def test(request):
	current_user = request.user
	print("")
	print("Current user: " + str(current_user))
	print("-------------------")
	print("User ID: " + str(current_user.id))
	print("Email:   " + str(current_user.email))
	print("=================================")
	print("")

	return HttpResponseRedirect("/utilities/")
@login_required(login_url="/login/")
def emailusers(request):
	if request.method=='POST':
		form = sendEmailForm(request.POST)
		message = form
		for i in form:
			print(i)
		print(form)
		myemailgeek  = "marcsageek@gmail.com"
		passwordgeek = "usmtfzbmbyudsvcr"
		print("  creating server")
		server = smtplib.SMTP("smtp.gmail.com", 587)
		print("  Starting ttls")
		server.starttls()
		print("  Logging in")
		server.login(myemailgeek, passwordgeek)
		# for i in Roommates.objects.all():
			# server.sendmail(str(myemailgeek), str(i.user.email), str(message))
		server.sendmail(str(myemailgeek), str("MarcStocker@outlook.com"), str(message))
		print("  Quitting Server")
		server.quit()
		print("Message sent")

		return HtmlResponseRedirect("/utilities/")
	else:
		form = sendEmailForm()
	context = {
		'page_name' :"Admin Email Panel",
		'sitename'  :"Roommate Homebase",
		'page_name' :"Email Users",
		'form'      :form,
	}
	return render(request, 'billing/sendemail.html', context)
@login_required(login_url="/login/")
def deleteallbills(request):
	print("Deleting all Requests, Bills, and payments")
	print("   Deleting PaymentRequests...")
	for i in PaymentRequest.objects.all():
		time.sleep(.1)
		i.delete()
	print("   Deleting UtilityBills...")
	for i in UtilityBill.objects.all():
		time.sleep(.1)
		i.delete()
	print("   Deleting userPayments...")
	for i in UserPayment.objects.all():
		time.sleep(.1)
		i.delete()
	print("   Deleting billPayments...")
	for i in BillPayment.objects.all():
		time.sleep(.1)
		i.delete()
	return HttpResponseRedirect("/utilities/admintablepage")
@login_required(login_url="/login/")
def deleterequests(request):
	print("\n\nDeleting lastest Requests, and Bill associated with it.\n")
	last_bill = UtilityBill.objects.all().reverse()[0]
	print("Last Bill= " + str(last_bill.id) + " - $" + str(last_bill.amount))
	lastid = last_bill.id
	recent_requests = PaymentRequest.objects.filter(UtilBill_id=lastid)
	for i in recent_requests:
		time.sleep(.2)
		i.delete()
	last_bill.delete()
	print("Selected Payment requests associated with Bill ID: " + str(lastid))
	return HttpResponseRedirect('/utilities/')
