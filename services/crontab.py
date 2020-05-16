from django.conf import settings
from crontab import CronTab
from cron import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from cron.models import Job
import os
import sys


class CrontabService:
    def __init__(self):
        self.cron = CronTab(user=True)

    def _get_curl_command(self, job):
        return f'{sys.executable} {os.path.join(settings.BASE_DIR, "manage.py")} sendrequest --job_id {job.id}'

    def createJob(self, dbJob):
        job = self.cron.new(command=self._get_curl_command(dbJob), comment=str(dbJob.id))
        job.setall(dbJob.timeExpression)
        self.cron.write()

    def removeJob(self, dbJob):
        job = self.cron.find_comment(str(dbJob.id))
        self.cron.remove(job)
        self.cron.write()

    def refreshAllJob(self):
        self.cron.remove_all()
        self.cron.write()
        for job in models.Job.objects.all():
            self.createJob(job)


CRON_SERVICE = CrontabService()


@receiver(post_save, sender=Job)
def print_only_after_deal_created(sender, instance, created, **kwargs):
    if not created:
        CRON_SERVICE.removeJob(instance)
    CRON_SERVICE.createJob(instance)
