from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from django.views.generic import TemplateView
from carrental.views import CarDetailView
from carrental.views import CarHomeView, CarBookingView

urlpatterns = [
    url(r'^$', CarHomeView.as_view(), name='car_home'),
    url(r'^detail/(?P<pk>\d+)/$', CarDetailView.as_view(), name='car_detail'),
    url(r'^booking/(?P<pk>\d+)/$', CarBookingView.as_view(), name='car_booking'),
]