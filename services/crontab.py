from crontab import CronTab
from cron import models

class CrontabService:
  def __init__(self):
    self.cron = CronTab(user=True)
  
  def _get_curl_command(self, job):
    return f'request_curl --url {job.fullURL} --token {job.application.token} --method {job.method} &> /var/log/poker.logs'

  def createJob(self, dbJob):
    job = self.cron.new(command = self._get_curl_command(dbJob), comment=str(dbJob.id))
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
