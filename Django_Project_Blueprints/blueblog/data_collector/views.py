from django.shortcuts import render

from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
# Create your views here.
from data_collector.models import DataPoint, Alert
# API endpoint
from django.forms.models import modelform_factory
from django.http.response import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.http.response import HttpResponseForbidden
from django.views.generic import View


class StatusView(TemplateView):
    template_name = 'data_collector/status.html'

    def get_context_data(self, **kwargs):
        ctx = super(StatusView, self).get_context_data(**kwargs)
        nodes_and_data_types = DataPoint.objects.all().values('node_name', 'data_type').distinct()
        status_data_dict = dict()
        alerts = Alert.objects.filter(is_active=True)
        for node_and_data_type_pair in nodes_and_data_types:
            node_name = node_and_data_type_pair['node_name']
            data_type = node_and_data_type_pair['data_type']
            latest_data_point = DataPoint.objects.filter(node_name=node_name, data_type=data_type).latest('datetime')
            latest_data_point.has_alert = self.point_does_have_alert(latest_data_point, alerts)
            # setdefault 设置node_name的默认值，并返回值
            data_point_map = status_data_dict.setdefault(node_name, dict())
            # data_point_map[data_type] = DataPoint.objects.filter(
            #     node_name=node_name, data_type=data_type
            # ).latest('datetime')
            data_point_map[data_type] = latest_data_point
        ctx['status_data_dict'] = status_data_dict
        return ctx

    def point_does_have_alert(self, data_point, alerts):
        for alert in alerts:
            if alert.node_name and data_point.node_name != alert.node_name:
                continue
            if alert.data_type != data_point.data_type:
                continue
            if alert.min_value is not None and data_point.data_value < alert.min_value:
                return True
            if alert.max_value is not None and data_point.data_value > alert.max_value:
                return True
            return False


class AlertListView(ListView):
    template_name = 'data_collector/alerts_list.html'
    model = Alert


class CreateAlertView(CreateView):
    template_name = "data_collector/update_or_create_alert.html"
    model = Alert
    fields = '__all__'

    def get_success_url(self):
        return reverse('alerts_list')


class UpdateAlertView(UpdateView):
    template_name = 'data_collector/update_or_create_alert.html'
    model = Alert
    fields = '__all__'

    def get_success_url(self):
        return reverse('alerts_list')


class DeleteAlertView(DeleteView):
    template_name = 'data_collector/delete_alert.html'
    model = Alert

    def get_success_url(self):
        return reverse('alerts_list')


# API endpoint
class RecordDataApiView(View):
    def post(self, request, *args, **kwargs):
        # Check if the secret key matches
        if request.META.get('HTTP_AUTH_SECRET') != 'supersecretkey':
            return HttpResponseForbidden('Auth key error.')
        form_class = modelform_factory(DataPoint, fields=['node_name', 'data_type', 'data_value'])
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
