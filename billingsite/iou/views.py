from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F, FloatField, Sum

from billing.models import Roommate, Lease

# from .models import PaymentRequest, Bill

# Create your views here.

def iouhome(request):
	if not Roommate.objects.filter(user_id=request.user.id):
		print("User is not associated with a house")
		context = { 'page_name':"Join a House"}
		return render(request, 'billing/joincreatehouse.html', context)

	print("\n\n\n\n==========================================================")
	print("def IOU Home(request)")
	print(">>>>>>>>>>>>>>>>>>>\n\n")

	cur_roommate = Roommate.objects.get(user=request.user.id)
	house        = cur_roommate.house
	my_roommates = Roommate.objects.filter(house_id=house.id).order_by('id')

	ioweTotal=0
	owedTotal=0
	roommateIOwe = {}
	roommateOwesMe = {}

	##for roommate in my_roommates:
		##if roommate != cur_roommate:
			##all_requests = PaymentRequest.objects.filter(requester_id=roommate.id, requestee_id=cur_roommate.id)
##
			##temptotbill = 0
			##temptotpay  = 0





	context = {
		"page_name"     :"IOU Home",
		"house"         :house,
		"my_roommates"  :my_roommates,
		"cur_roommate"  :cur_roommate,


	}

	return render(request, 'iou/iouhome.html', context)
