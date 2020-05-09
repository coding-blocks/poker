from django.contrib import admin
from django.urls import path
from services import crontab

urlpatterns = [
    path('admin/', admin.site.urls),
]

try: 
    CRON_SERVICE = crontab.CrontabService()
    CRON_SERVICE.refreshAllJob()
except:
    pass
