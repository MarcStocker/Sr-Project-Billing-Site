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

# import pandas as pd

# Create your views here.

def home(request):
    random.seed()
    randomnumber=random.randint(0,100)
    print(randomnumber)

    cwd=os.getcwd()
    print(cwd)
    context = {
        'randnum':randomnumber,
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
    }
    return render(request, 'billingsite/register.html', context)
