from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    #<WebSite.com>/register/
    url(r'register$', views.register, name="register"),
]
