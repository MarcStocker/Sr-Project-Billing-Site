from django.conf.urls import url
from . import views, viewstest

app_name = 'billing'

urlpatterns = [
    #<WebSite.com>/utilities/
    url(r'^$', views.billinghome, name="billinghome"),


    # Edit/Add Information
    #-------------------------------------------
    #<WebSite.com>/utilities/addUserPayment/
    # url(r'^addUserPayment/$', views.adduserpayment, name="adduserpayment"),

    #<WebSite.com>/utilities/addBillPayment/
    # url(r'^addBillPayment/$', views.addbillpayment, name="addbillpayment"),

    #<WebSite.com>/utilities/addUtilityBill/
    url(r'^addBill/$', views.addbill, name="addbill"),
    #<WebSite.com>/utilities/addUtilityBill/
    url(r'^addBillPayment/$', views.addbillpayment, name="addbillpayment"),
    #<WebSite.com>/utilities/addUtilityBill/
    url(r'^addUserPayment/$', views.adduserpayment, name="adduserpayment"),

    #<WebSite.com>/utilities/addLease/
    url(r'^addLease/$', views.addlease, name="addlease"),
    #<WebSite.com>/utilities/addRoommate/
    url(r'^addRoommate/$', views.addroommate, name="addroommate"),
    #<WebSite.com>/utilities/addRoommate/
    url(r'^addSelf/$', views.addself, name="addself"),

    #<WebSite.com>/utilities/admintablepage/
    url(r'^admintablepage/$', views.admintablepage, name="admintablepage"),





    #<WebSite.com>/billing/test/
    url(r'^test/$', viewstest.test, name="test"),
    url(r'^deleteallbills$', views.deleteallbills, name="deleteallbills"),
    url(r'^emailusers/$', views.emailusers, name="emailusers"),


    url(r'^deleterequests/$', views.deleterequests, name="deleterequests"),
]
