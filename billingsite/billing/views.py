from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Lease, Roommate, UtilityBill
from .models import UtilityType, billPayment, userPayment
from .models import PaymentRequest
from .forms import UserPaymentForm, addUtilityTypeForm
from .forms import addUtilityBillPaymentForm, addNewBillForm
from .forms import addLeaseForm, addRoommateForm
from .forms import addNewBillPaymentForm, addNewUserPaymentForm

from decimal import *

import random
import os

# Create your views here.
@login_required(login_url="/login/")
def billinghome(request):

    print("\n\n\n\n==========================================================")
    print("def billinghome(request)")
    print(">>>>>>>>>>>>>>>>>>>\n\n")
    cur_roommate = Roommate.objects.get(user=request.user.id)
    house        = cur_roommate.house
    my_roommates = Roommate.objects.filter(house_id=house.id)

    # TODO - Total Owed Overall - # DONE
    my_roommatespaid={}
    for i in my_roommates:
        my_roommatespaid[i.name]=i.getPercentPaid()
        # print(i.name + " has paid "+ str(my_roommatespaid[i.name]) + "%")
    # TODO - Debt Tab
    roommates_iowe       = {}
    roommate_collections = {}
    for i in my_roommates:
        if i.id != cur_roommate.id:
            # Code for Roommates_iowe
            all_requests = PaymentRequest.objects.filter(requester_id=i.id, requestee_id=cur_roommate.id)
            userpayments = userPayment.objects.filter(payee_id=i.id, payer_id=cur_roommate.id)
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
            userpayments = userPayment.objects.filter(payee_id=cur_roommate.id, payer_id=i.id)
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
            elif temptotstillowed < 0:
                roommates_iowe[i.name] = [temptotcollections, temptotpayments, temptotstillowed]





    # TODO - Total Collections of Current User
    curuser_collect=cur_roommate.getTotCollections()
    # TODO - Total Debt Of Current User
    curuser_debt=cur_roommate.getTotDebt()
    totmoney = curuser_collect - curuser_debt
    # TODO - Display all Bill by month in new Tab
    # TODO - Display all Payments for each user in a new Tab


    numroommates= 0

    roommateowes=[]
    roommatepaid=[]

    # TODO - All Bills Associated With House
    all_bills = UtilityBill.objects.filter(house_id=house.id)
    all_bills = all_bills.order_by('-dueDate')
    last5bills= all_bills.order_by('-dueDate')[:5]

    #
    all_payments    = userPayment.objects.all()
    house_payments  = []
    for i in my_roommates:
        for j in all_payments:
            if j.payer.house.id == house.id:
                house_payments.append(j)

    print("\n-------------------\n      END \n-------------------\n END BILLING HOME \n-------------------\n\n")
    context = {
        'page_name'         :"Utilities - Roommate Homebase",
        'house'             :house,
        'totmoney'          :totmoney,
        'all_bills'         :all_bills,
        'last5bills'        :last5bills,
        'all_payments'       :all_payments,
        'curuser_debt'      :curuser_debt,
        'numroommates'      :numroommates,
        'roommateowes'      :roommateowes,
        'roommatepaid'      :roommatepaid,
        'my_roommates'      :my_roommates,
        'roommates_iowe'    :roommates_iowe,
        'curuser_collect'   :curuser_collect,
        'my_roommatespaid'  :my_roommatespaid,
        'roommate_collections':roommate_collections,
    }
    return render(request, 'billing/billinghome.html', context)

# @login_required(login_url="/login/")
# def billinghome(request):
    #     #Overview is for house id=
    #     cur_user=request.user
    #     print("CURRENT USER IS: "+str(cur_user.username))
    #     houseid=1
    #     numroommates=5
    #     my_roommates=[]
    #     roommatepaid=[]
    #     money_owed=[]
    #     all_roommates=Roommate.objects.all()
    #     all_userpayments=userPayment.objects.all()
    #     all_billpayments=billPayment.objects.all()
    #     all_bills=UtilityBill.objects.all()
    #     all_houses=Lease.objects.all()
    #     print("======")
    #     print("======")
    #     print("======")
    #     for i in all_houses:
    #         if i.id == houseid:
    #             print("--- Retrieving Data for House :", i.name, " - ID:", houseid)
    #     inum=0
    #
    #     # Collect total owed for entire house
    #     totalowed=0
    #     for i in all_bills:
    #         if i.house == houseid:
    #             totalowed+=i.amount
    #
    #     # Amount each Roommate has paid
    #     for i in all_roommates:
    #         if i.house.id == 1:
    #             my_roommates.append(i.id)
    #             totalpaid=0
    #             for j in all_userpayments:
    #                 if j.payer.id == i.id:
    #                     totalpaid+=j.amount
    #             for j in all_billpayments:
    #                 if j.payer.id == i.id:
    #                     totalpaid+=j.amount/numroommates
    #             roommatepaid.append(totalpaid)
    #
    #     print("------------- Roommate Paid ------------------")
    #     for i in roommatepaid:
    #         print(i)
    #
    #     housetotal=0
    #     for i in all_houses:
    #         if i.id == houseid:
    #             for j in all_bills:
    #                 if j.house.id == houseid:
    #                     housetotal+=j.amount
    #     print("------------- Total Bills For House ------------------")
    #     print("$", housetotal)
    #
    #     perroommate=housetotal/numroommates
    #     perroommate=round(perroommate,2)
    #     print("------------- Total Owed Per Roommate ------------------")
    #     print("$", perroommate)
    #
    #     roommateowes=[]
    #     iternum=0
    #     for i in roommatepaid:
    #         roommateowes.append(round(perroommate-i,2))
    #
    #     print("------------- Total Owed for each Roommate ------------------")
    #     for i in roommateowes:
    #         print("$", i)
    #
    #     percentowed=[]
    #     for i in range(0,int(numroommates)):
    #         tempnum=roommateowes[i]-roommatepaid[i]
    #         tempnum=tempnum/roommateowes[i]
    #         tempnum=tempnum*100
    #         percentowed.append(round(tempnum,0))
    #
    #     print("------------- Percent Still Owed ------------------")
    #     for i in percentowed:
    #         print(str(i)+"%")
    #
    #     for i in all_roommates:
    #         if i.house.id == houseid:
    #             print("User: " + str(i.name))
    #             print("  Owes: " + str(i.getPercentOwed()))
    #
    #
    #
    #
    #
    #     debt=56.32
    #     collections=143.43
    #     totmoney=collections-debt
    #     totmoney=round(totmoney,2)
    #
    #     context = {
    #         'debt':debt,
    #         'collections':collections,
    #         'totmoney':totmoney,
    #         'numroommates':numroommates,
    #         'roommateowes':roommateowes,
    #         'roommatepaid':roommatepaid,
    #         'all_roommates':all_roommates,
    #     }
    #     return render(request, 'billing/billinghome.html', context)

def addbill(request):
    if request.method=='POST':
        form = addNewBillForm(request.POST, request.FILES)
        if form.is_valid():
            j = form.save(request)
            j.save()
            j.createRequests()

            return HttpResponseRedirect('/utilities/admintablepage/')
    else:
        form = addNewBillForm()
    context = {
        'page_name' :"Add New Bill - Roommate Homebase",
        'sitename'  :"Roommate Homebase",
        'page_name' :"Add a Bill",
        'form':form,
    }
    return render(request, 'billing/addBill.html', context)

def addbilltype(request):
    if request.method=='POST':
        form = addUtilityTypeForm(request.POST)
        if form.is_valid():
            j = form.save(request, commit=False)
            j.save()
            return HttpResponseRedirect('/utilities/admintablepage/')
    else:
        form = addNewBillForm()
    context = {
        'page_name' :"Add a New Bill Type - Roommate Homebase",
        'sitename'  :"Roommate Homebase",
        'page_name' :"Add a Bill Payment",
        'form'      :form,
    }
    return render(request, 'billing/addBill.html', context)

def addbillpayment(request):
    if request.method=='POST':
        form = addNewBillPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            j = form.save(request)
            j.save()
            return HttpResponseRedirect('/utilities/admintablepage/')
    else:
        form = addNewBillPaymentForm()
    context = {
        'page_name' :"Add Bill Payment - Roommate Homebase",
        'sitename'  :"Roommate Homebase",
        'page_name' :"Add a Bill Payment",
        'form'      :form,
    }
    return render(request, 'billing/addBillPayment.html', context)

def adduserpayment(request):
    if request.method=='POST':
        form = addNewUserPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            j = form.save(request)
            j.save()
            return HttpResponseRedirect('/utilities/admintablepage/')
    else:
        form = addNewUserPaymentForm()
    context = {
        'page_name' :"Add User Payment - Roommate Homebase",
        'sitename'  :"Roommate Homebase",
        'page_name' :"Add a User Payment",
        'form'      :form,
    }
    return render(request, 'billing/addUserPayment.html', context)

def addlease(request):
    if request.method=='POST':
        form = addLeaseForm(request.POST)
        if form.is_valid():
            j = form.save(request)
            j.save()
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
        'page_name' :"Add Roommate - Roommate Homebase",
        'sitename'  :"Roommate Homebase",
        'page_name' :"Add a Roommate",
        'form'      :form,
    }
    return render(request, 'billing/addRoommate.html', context)

def admintablepage(request):
    all_users           = User.objects.all()
    all_leases          = Lease.objects.all()
    all_roommates       = Roommate.objects.all()
    all_userpayments    = userPayment.objects.all()
    all_billpayments    = billPayment.objects.all()
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

def test(request):
    current_user = request.user
    print("")
    print("Current user: " + str(current_user))
    print("-------------------")
    print("User ID: " + str(current_user.id))
    print("Email:   " + str(current_user.email))
    print("=================================")
    print("")
    all_users = User.objects.all()
    for i in all_users:
        print("User name:  " + str(i.username))
        print("User ID:    " + str(i.id))
        if i.email != "":
            print("User email: " + str(i.email))
        print("---")
    user2 = User.objects.get(pk=2)
    print("")

    return HttpResponseRedirect("/utilities/")
