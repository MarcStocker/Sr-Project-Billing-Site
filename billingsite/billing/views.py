from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Lease, Roommate, UtilityBill
from .models import UtilityType, billPayment, userPayment
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
    #Overview is for house id=
    houseid=1
    numroommates=5
    my_roommates=[]
    roommatepaid=[]
    money_owed=[]
    all_roommates=Roommate.objects.all()
    all_userpayments=userPayment.objects.all()
    all_billpayments=billPayment.objects.all()
    all_bills=UtilityBill.objects.all()
    all_houses=Lease.objects.all()
    print("======")
    print("======")
    print("======")
    for i in all_houses:
        if i.id == houseid:
            print("--- Retrieving Data for House :", i.name, " - ID:", houseid)
    inum=0
    #Collect total owed for entire house
    totalowed=0
    for i in all_bills:
        if i.house == houseid:
            totalowed+=i.amount

    # Amount each Roommate has paid
    for i in all_roommates:
        if i.house.id == 1:
            my_roommates.append(i.id)
            totalpaid=0
            for j in all_userpayments:
                if j.payer.id == i.id:
                    totalpaid+=j.amount
            for j in all_billpayments:
                if j.payer.id == i.id:
                    totalpaid+=j.amount/numroommates
            roommatepaid.append(totalpaid)

    print("------------- Roommate Paid ------------------")
    for i in roommatepaid:
        print(i)

    housetotal=0
    for i in all_houses:
        if i.id == houseid:
            for j in all_bills:
                if j.house.id == houseid:
                    housetotal+=j.amount
    print("------------- Total Bills For House ------------------")
    print("$", housetotal)

    perroommate=housetotal/numroommates
    perroommate=round(perroommate,2)
    print("------------- Total Owed Per Roommate ------------------")
    print("$", perroommate)

    roommateowes=[]
    iternum=0
    for i in roommatepaid:
        roommateowes.append(round(perroommate-i,2))

    print("------------- Total Owed for each Roommate ------------------")
    for i in roommateowes:
        print("$", i)

    percentowed=[]
    for i in range(0,int(numroommates)):
        tempnum=roommateowes[i]-roommatepaid[i]
        tempnum=tempnum/roommateowes[i]
        tempnum=tempnum*100
        percentowed.append(round(tempnum,0))

    print("------------- Percent Still Owed ------------------")
    for i in percentowed:
        print(str(i)+"%")




    debt=56.32
    collections=143.43
    totmoney=collections-debt
    totmoney=round(totmoney,2)
    context = {
        'debt':debt,
        'collections':collections,
        'totmoney':totmoney,
        'numroommates':numroommates,
        'roommateowes':roommateowes,
        'roommatepaid':roommatepaid,
    }
    return render(request, 'billing/billinghome.html', context)

def addbill(request):
    if request.method=='POST':
        form = addNewBillForm(request.POST, request.FILES)
        if form.is_valid():
            j = form.save(request)
            j.save()
            return HttpResponseRedirect('/utilities/admintablepage/')
    else:
        form = addNewBillForm()
    context = {
        'sitename':"Roommate Homebase",
        'page_name':"Add a Bill",
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
        'sitename':"Roommate Homebase",
        'page_name':"Add a Bill Payment",
        'form':form,
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
        'sitename':"Roommate Homebase",
        'page_name':"Add a Bill Payment",
        'form':form,
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
        'sitename':"Roommate Homebase",
        'page_name':"Add a User Payment",
        'form':form,
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
        'sitename':"Roommate Homebase",
        'page_name':"Add a Lease",
        'form':form,
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
        'sitename':"Roommate Homebase",
        'page_name':"Add a Roommate",
        'form':form,
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

    context = {
        'sitename':"Roommate Homebase",
        'page_name':"Admin - All Tables",
        'all_users':all_users,
        'all_leases':all_leases,
        'all_roommates':all_roommates,
        'all_userpayments':all_userpayments,
        'all_billpayments':all_billpayments,
        'all_utilityBills':all_utilityBills,
        'all_utilityTypes':all_utilityTypes,
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






# def adduserpayment(request):
    #     if request.method=='POST':
    #         form = UserPaymentForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             j = form.save(request, commit=False)
    #             j.save()
    #             return HttpResponseRedirect('/billing/billinghome/')
    #     else:
    #         form = UserPaymentForm()
    #     context = {
    #         'sitename':"Roommate Homebase",
    #         'page_name':"Add a User Payment",
    #         'form':form,
    #     }
    #     return render(request, 'billing/addUserPayment.html')
    #
    # def addbillpayment(request):
    #     if request.method=='POST':
    #         form = addUtilityBillForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             j = form.save(request, commit=False)
    #             j.save()
    #             return HttpResponseRedirect('/billing/billinghome/')
    #     else:
    #         form = UtilityBillPaymentForm()
    #     context = {
    #         'sitename':"Roommate Homebase",
    #         'page_name':"Add a Bill Payment",
    #         'form':form,
    #     }
    #     return render(request, 'billing/addBillPayment.html')
    #
