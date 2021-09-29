from django.db import models
import urllib.parse


METHODS = (
  ('GET', 'GET'),
  ('POST', 'POST')
)


# Create your models here.
class Application(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=1024)
  callbackURL = models.URLField()
  token = models.CharField(max_length=1024)

  def __str__(self):
    return self.name


class Job(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=1024)
  application = models.ForeignKey(Application, on_delete=models.CASCADE)
  method = models.CharField(max_length=10, choices=METHODS)
  endpoint = models.CharField(max_length=1024)
  timeExpression = models.CharField(max_length=1024)
  isPaused = models.BooleanField(default=False)

  @property
  def fullURL(self):
    print(self.application.callbackURL)
    return urllib.parse.urljoin(self.application.callbackURL, self.endpoint)

  @property
  def lastExecutionResult(self):
    lastExecuted = self.log_set.last()
    return lastExecuted.statusCode if lastExecuted else None

  def __str__(self):
    return self.name


class Log(models.Model):
  id = models.AutoField(primary_key=True)
  job = models.ForeignKey(Job, on_delete=models.CASCADE)
  statusCode = models.IntegerField()
  response = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  @property
  def isSuccessful(self):
    return (self.statusCode // 100) == 2

  def __str__(self):
    return f'{self.job.name}-{self.id}'
