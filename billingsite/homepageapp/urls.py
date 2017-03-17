
from django.conf.urls import url
from . import views, viewstest

app_name = 'homepageapp'

urlpatterns = [
    #<WebSite.com>/
    url(r'^$', views.home, name="home"),
    #<WebSite.com>/home/
    url(r'^home/$', views.home, name="home"),
]
