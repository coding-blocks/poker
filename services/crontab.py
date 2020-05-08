from crontab import CronTab
from cron import models

class CrontabService:
  def __init__(self):
    self.cron = CronTab()
  
  def _get_curl_command(self, job):
    return f'./scripts/request_curl.py --url {job.fullURL} --token {job.application.token} --method {job.method}'

  def createJob(self, dbJob):
    job = self.cron.new(command = self._get_curl_command(dbJob), comment=str(dbJob.id))
    job.set(job.timeExpression)
    cron.write()
  
  def removeJob(self, dbJob):
    job = self.cron.find_comment(str(dbJob.id))
    cron.remove(job)
    cron.write()

  def refreshAllJob(self):
    self.cron.remove_all()
    self.cron.write()
    for job in models.Job.objects.all():
      self.createJob(job)
