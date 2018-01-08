from django.shortcuts import render

# Create your views here.
from carrental.models import Car, Booking
from django.views.generic import DetailView, TemplateView, CreateView


class CarHomeView(TemplateView):
    template_name = 'carrental/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(CarHomeView, self).get_context_data(**kwargs)
        cars = Car.objects.filter(is_available=True)
        ctx['cars'] = cars
        return ctx


class CarDetailView(DetailView):
    template_name = 'carrental/car_detail.html'
    model = Car

    def get_context_data(self, **kwargs):
        ctx = super(CarDetailView, self).get_context_data(**kwargs)
        if 'booking-success' in self.request.GET:
            ctx['booking_success'] = 'booking success'
        return ctx


class CarBookingView(CreateView):
    template_name = 'carrental/car_booking.html'
    model = Booking
    fields = ['customer_name',
              'customer_phone',
              'customer_email',
              'booking_start',
              'booking_end',
              'booking_message']

    def get_car(self):
        car_pk = self.kwargs['pk']
        car = Car.objects.get(pk=car_pk)
        return car

    def get_context_data(self, **kwargs):
        ctx = super(CarBookingView, self).get_context_data(**kwargs)
        ctx['car'] = self.get_car()
        return ctx

    def form_valid(self, form):
        new_booking = form.save(commit=False)
        new_booking.car = self.get_car()
        new_booking.is_approved = False
        new_booking.save()
        return super(CarBookingView, self).form_valid(form)

    def get_success_url(self):
        car = self.get_car()
        car_detail_page_url = car.get_absolute_url()

        return '{}?booking-success=1'.format(car_detail_page_url)
