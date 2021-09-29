from django.contrib import admin, messages

from cron import models
from cron.tasks import execute_job


# Register your models here.
@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
  actions = ['execute_now']
  list_display = ['name', 'application', 'method', 'endpoint', 'timeExpression', 'lastExecutionResult', 'isPaused']

  def execute_now(self, request, queryset):
    for query in queryset:
      execute_job.delay(query.id)
      self.message_user(request, f'successfully executed job {query.name}', messages.SUCCESS)


admin.site.register([
  models.Application,
  models.Log
])
