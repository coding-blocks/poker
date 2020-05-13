from django.contrib import admin
from django.urls import path, include
from oneauth.views import login_view
from services import crontab

urlpatterns = [
  path('admin/login/', login_view),
  path('admin/', admin.site.urls),
  path('oneauth/', include('oneauth.urls')),
]

try:
  CRON_SERVICE = crontab.CrontabService()
  CRON_SERVICE.refreshAllJob()
except:
  pass
