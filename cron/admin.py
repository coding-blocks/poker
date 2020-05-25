from django.contrib import admin, messages
from django.core.management import call_command

from cron import models


# Register your models here.
@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
  actions = ['execute_now']
  list_display = ['name', 'application', 'method', 'endpoint', 'timeExpression', 'lastExecutionResult']

  def execute_now(self, request, queryset):
    for query in queryset:
      call_command('sendrequest', job_id=query.id)
      self.message_user(request, f'successfully executed job {query.name}', messages.SUCCESS)


admin.site.register([
  models.Application,
  models.Log
])
