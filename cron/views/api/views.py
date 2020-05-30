import requests
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from cron.models import Job, Log


class JobExecuteAPIView(APIView):
  def post(self, request, pk):
    job = get_object_or_404(Job, pk=pk)
    headers = {
      'Authorization': f'Bearer {job.application.token}'
    }
    session = requests.Session()
    request = requests.Request(job.method, job.fullURL, headers=headers).prepare()
    response = session.send(request)
    Log.objects.create(job=job, statusCode=response.status_code, response=response.text)
    return Response({'status': 'successful'}, status=200)
