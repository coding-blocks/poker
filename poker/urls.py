from django.contrib import admin
from django.urls import path
from services import crontab
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from oneauth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    url(r'^callback/$', views.callback, name='callback'),
]

try: 
    CRON_SERVICE = crontab.CrontabService()
    CRON_SERVICE.refreshAllJob()
except:
    pass
