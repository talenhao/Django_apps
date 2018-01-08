from django.db import models

# Create your models here.
from django.core.urlresolvers import reverse


class Car(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='car_images')
    description = models.TextField()
    daily_rent = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Booking(models.Model):
    car = models.ForeignKey(Car)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.TextField()
    customer_email = models.EmailField()

    booking_start = models.DateField()
    booking_end = models.DateField()
    booking_message = models.TextField()

    is_approved = models.BooleanField()

