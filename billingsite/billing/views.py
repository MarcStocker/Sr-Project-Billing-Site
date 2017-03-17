from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Lease, Roommate, UtilityBill
from .models import UtilityType, billPayment, userPayment
from .forms import UserPaymentForm, addUtilityBillForm
from .forms import addUtilityBillPaymentForm, addNewBillForm

from decimal import *

import random
import os

# Create your views here.
def billinghome(request):
    random.seed()
    randomnumber=random.randint(0,100)

    debt=56.32
    collections=143.43
    totmoney=collections-debt
    totmoney=round(totmoney,2)
    context = {
        'randnum':randomnumber,
        'debt':debt,
        'collections':collections,
        'totmoney':totmoney,
    }
    return render(request, 'billing/billinghome.html', context)

def addbill(request):
    if request.method=='POST':
        form = addNewBillForm(request.POST, request.FILES)
        if form.is_valid():
            j = form.save(request, commit=False)
            j.save()
            return HttpResponseRedirect('/billing/billinghome/')
    else:
        form = addNewBillForm()
    context = {
        'sitename':"Roommate Homebase",
        'page_name':"Add a Bill Payment",
        'form':form,
    }
    return render(request, 'billing/addBill.html', context)

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
