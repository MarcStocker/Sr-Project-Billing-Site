from django.conf.urls import url
from . import views, viewstest

app_name = 'billing'

urlpatterns = [
    #<WebSite.com>/utilities/
    url(r'^$', views.billinghome, name="billinghome"),


    # Edit/Add Information
    #<WebSite.com>/utilities/addUserPayment/
    url(r'^addUserPayment/$', views.adduserpayment, name="adduserpayment"),
    #<WebSite.com>/utilities/addBillPayment/
    url(r'^addBillPayment/$', views.addbillpayment, name="addbillpayment"),






    #<WebSite.com>/billing/test/
    url(r'^test/$', viewstest.test, name="test"),
]
