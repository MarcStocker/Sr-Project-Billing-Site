from django.conf.urls import url
from . import views

app_name = 'iou'

urlpatterns = [
    #<WebSite.com>/iou/
    url(r'^$', views.iouhome, name="iouhome"),
]
