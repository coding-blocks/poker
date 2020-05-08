from django.contrib import admin
from cron import models

# Register your models here.
admin.site.register([
  models.Application,
  models.Job,
  models.Log
])
