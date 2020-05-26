from django.urls import path

from cron.views.api.views import *

urlpatterns = [
  path('job/execute/<int:pk>/', JobExecuteAPIView.as_view(), name='application-list'),
]
