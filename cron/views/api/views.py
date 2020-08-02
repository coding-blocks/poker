from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cron.models import Job
from cron.tasks import execute_job


class JobExecuteAPIView(APIView):
  def post(self, request, pk):
    get_object_or_404(Job, pk=pk)
    execute_job.delay(pk)
    return Response('job will be executed shortly', status=status.HTTP_200_OK)
