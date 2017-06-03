from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import random
import os
import subprocess


def test(request):
	current_user = request.user
	print("////////////////////////////////////////////////////////////////////////////////////////////////////")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("~~~~~~~         BEGIN Test       ~~~~~~~~~~~")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

	print("Current user: " + str(current_user))
	print("-------------------")
	print("User ID: " + str(current_user.id))
	print("Date_Created: " + str(current_user.date_joined))
	print("Year: " + str(current_user.date_joined.strftime('%Y')))
	print("Month: " + str(current_user.date_joined.strftime('%m')))
	print("Date: " + str(current_user.date_joined.strftime('%d')))
	print("Day: " + str(current_user.date_joined.strftime('%w')))


	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("~~~~~~~          END Test        ~~~~~~~~~~~")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
	return HttpResponseRedirect("/utilities/")
