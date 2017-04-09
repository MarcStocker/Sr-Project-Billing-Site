from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import random
import os

from django.contrib.auth import authenticate, login
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.utils.html import escape
from django.http import JsonResponse
import datetime
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from billing.forms import UtilityBill, Roommate

# import pandas as pd

# Create your views here.

def home(request):

    # random.seed()
    # randomnumber=random.randint(0,100)
    # print(randomnumber)
    # cwd=os.getcwd()
    # print(cwd)

    if request.user.is_authenticated():
        if Roommate.objects.filter(user_id=request.user.id).exists() == True:
            cur_roommate = Roommate.objects.get(user_id=request.user.id)
            house        = cur_roommate.house
            last5bills   = UtilityBill.objects.filter(house_id=house.id)
            last5bills   = last5bills.order_by('-dueDate')[:5]
            my_roommates = Roommate.objects.filter(house_id=house.id)
            context = {
            'page_name'     :"Home - Roommate Homebase",
            'last5bills'    :last5bills,
            'my_roommates'  :my_roommates,
            }
        else:
            context = {
            'page_name' :"Home - Roommate Homebase",
            # 'randnum'   :randomnumber,
            }
    else:
        context = {
        'page_name' :"Home - Roommate Homebase",
        # 'randnum'   :randomnumber,
        }

    return render(request, 'homepageapp/homepage.html', context)

def register(request):
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            print(login(request, user))
            return HttpResponseRedirect('/')
    else:
        form = RegisterForm
        print("something")
        # form = blog_entry()

        context = {
        'page_name':"Register",
        'form':form,
        'page_name' :"Register - Roommate Homebase",
        }
        return render(request, 'billingsite/register.html', context)
