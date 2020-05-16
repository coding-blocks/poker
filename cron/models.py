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


class Job(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=1024)
  application = models.ForeignKey(Application, on_delete=models.CASCADE)
  method = models.CharField(max_length=10, choices=METHODS)
  endpoint = models.CharField(max_length=1024)
  timeExpression = models.CharField(max_length=1024)

  @property
  def fullURL(self):
    return urllib.parse.urljoin(self.application.callbackURL, self.endpoint)


class Log(models.Model):
  id = models.AutoField(primary_key=True)
  job = models.ForeignKey(Job, on_delete=models.CASCADE)
  statusCode = models.IntegerField()
  response = models.TextField()

  @property
  def isSuccessful(self):
    return (self.statusCode // 100) == 2
