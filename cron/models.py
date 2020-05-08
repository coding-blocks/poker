from django.db import models

# Create your models here.
class Application(models.Model):
  name = models.CharField(max_length = 1024)
  callbackURL = models.URLField()
  token = models.CharField(max_length = 1024)
  
class Job(models.Model):
  name = models.CharField(max_length = 1024)
  application = models.ForeignKey(Application, on_delete = models.CASCADE)
  endpoint = models.CharField(max_length = 1024)
  timeExpression = models.CharField(max_length = 1024)

class Log(models.Model):
  job = models.ForeignKey(Job, on_delete = models.CASCADE)
  statusCode = models.IntegerField()
  response = models.TextField()

  @property
  def isSuccessful(self):
    return (self.statusCode // 100) == 2
