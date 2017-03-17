from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import random
import os
import subprocess


def test(request):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~         BEGIN Test       ~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    random.seed()
    randomnumber=random.randint(0,100)
    print(" Random number: ", randomnumber)
    cwd=os.getcwd()
    print(" Directory:", cwd)

    print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("")
    print(" =======================")
    print(" == Running importcsv ==")
    print(" =======================")
    print("")
    print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    fields=['ID','Name','Payment Type','Amount','Pay To','Date','Details']
    print(" ---- Reading from Payments.cvs ----")
    # paymentsdf=pd.read_cvs('Payments.cvs',skipinitialspace=True,usecols=fields,encoding="ISO-8859-1")
    # print(paymentsdf)

    print(subprocess.check_output(['ls']))



    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~          END Test        ~~~~~~~~~~~")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return HttpResponseRedirect("/utilities/")
