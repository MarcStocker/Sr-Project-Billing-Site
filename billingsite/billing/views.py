from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

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

def adduserpayment(request):
    if request.method=='POST':
        form = UserPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            j = form.save(request, commit=False)
            j.save()
            return HttpResponseRedirect('/billing/billinghome/')
    else:
        form = UserPaymentForm()
    context = {
        'sitename':"Roommate Homebase",
        'page_name':"Add a User Payment",
        'form':form,
    }
    return render(request, 'addUserPayment.html')

def addbillpayment(request):
    if request.method=='POST':
        form = UtilityBillPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            j = form.save(request, commit=False)
            j.save()
            return HttpResponseRedirect('/billing/billinghome/')
    else:
        form = UtilityBillPaymentForm()
    context = {
        'sitename':"Roommate Homebase",
        'page_name':"Add a Bill Payment",
        'form':form,
    }
    return render(request, 'addBillPayment.html')
