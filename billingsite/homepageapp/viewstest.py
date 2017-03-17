from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import random
import os


def test(request):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~         BEGIN Test       ~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    return HttpResponseRedirect("/utilities/")
    random.seed()
    randomnumber=random.randint(0,100)
    print("Random number:")
    print(randomnumber)

    cwd=os.getcwd()
    print("Directory:")
    print(cwd)


    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("")
    print("=======================")
    print("== Running importcsv ==")
    print("=======================")
    print("")

    fields=['ID','Name','Payment Type','Amount','Pay To','Date','Details']

    print("---- Reading from Payments.cvs ----")
    # paymentsdf=pd.read_cvs('Payments.cvs',skipinitialspace=True,usecols=fields,encoding="ISO-8859-1")

    # print(paymentsdf)


    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~          END Test        ~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return HttpResponseRedirect("/utilities/")
