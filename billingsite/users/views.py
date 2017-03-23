from django.shortcuts import render
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse
from django.utils.html import escape
import datetime
from django.contrib.auth.decorators import login_required

from .forms import *

from django.contrib.auth import authenticate, login

# Create your views here.

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
    context = {
        'page_name':"Register",
        'form':form,
    }
    return render(request, 'register.html', context)
