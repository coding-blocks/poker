from django.urls import path

from cron.views.pages.views import *

urlpatterns = [
  path('application/', ApplicationListView.as_view(), name='application-list'),
  path('application/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
  path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail')
]
