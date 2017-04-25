"""billingsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views

from users.forms import LoginForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Login URL
    url(r'^login/', views.login, {'template_name':'billingsite/login.html','authentication_form':LoginForm}, name='login'),
    # Log out URL
    url(r'^logout/', views.logout,{'next_page':'/login'}),

    # Home, etc. URLS
    url(r'^', include('homepageapp.urls')),
    url(r'^home/', include('homepageapp.urls')),

    # Website App URLS
    url(r'^utilities/', include('billing.urls')),
    url(r'^ious/', include('iou.urls')),
    # url(r'^chores/', include('chores.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
