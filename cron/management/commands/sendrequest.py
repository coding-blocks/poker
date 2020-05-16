from multiprocessing.pool import job_counter

import requests
from django.core.management import BaseCommand

from cron.models import Log


class Command(BaseCommand):
    help = 'Sends GET/POST request to a given URL'

    def add_arguments(self, parser):
        parser.add_argument('--url', required=True)
        parser.add_argument('--token', required=True)
        parser.add_argument('--method', required=True, choices=['GET', 'POST'])

    def handle(self, *args, **options):
        headers = {
            'Authorization': f'Bearer {options["token"]}'
        }

        session = requests.Session()
        request = requests.Request(options['method'], options['url'], headers=headers).prepare()
        response = session.send(request)
        self.stdout.write(response.text)
        # Log.objects.create(job_id=,statusCode=response.status_code,response=response.text)
