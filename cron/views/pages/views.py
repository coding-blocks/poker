from django.views import generic
from django.views.generic.list import MultipleObjectMixin

from cron.models import Application, Job


class ApplicationListView(generic.ListView):
  model = Application
  paginate_by = 10


class ApplicationDetailView(generic.DetailView, MultipleObjectMixin):
  model = Application
  paginate_by = 10

  def get_context_data(self, **kwargs):
    object_list = self.get_object().job_set.order_by('pk')
    context = super(ApplicationDetailView, self).get_context_data(object_list=object_list, **kwargs)
    return context


class JobDetailView(generic.DetailView, MultipleObjectMixin):
  model = Job
  paginate_by = 10

  def get_context_data(self, **kwargs):
    log_queryset = self.get_object().log_set
    object_list = log_queryset.order_by('pk')
    success_count = log_queryset.filter(response__range=(200, 299)).count()
    total_count = log_queryset.count()
    context = super(JobDetailView, self).get_context_data(object_list=object_list,
                                                          success_rate=success_count / total_count * 100, **kwargs)
    return context
