import requests
from django.core.management import BaseCommand
from requests.exceptions import ConnectionError
from cron.models import Log, Job


class Command(BaseCommand):
  help = 'Sends GET/POST request to a given URL'

  def add_arguments(self, parser):
    parser.add_argument('--job_id', required=True, type=int)

  def handle(self, *args, **options):
    job = Job.objects.get(id=options['job_id'])
    headers = {
      'Authorization': f'Bearer {job.application.token}'
    }
    session = requests.Session()
    request = requests.Request(job.method, job.fullURL, headers=headers).prepare()
    try:
      response = session.send(request)
      Log.objects.create(job=job, statusCode=response.status_code, response=response.text)
    except ConnectionError:
      self.stderr.write('connection error')
