from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import random
import os

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
