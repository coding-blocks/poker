from celery import shared_task
from django.core.management import call_command


@shared_task
def execute_job(job_id):
  call_command('sendrequest', job_id=job_id)
