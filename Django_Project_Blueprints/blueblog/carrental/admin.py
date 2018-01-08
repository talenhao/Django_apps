from django.contrib import admin

# Register your models here.

from carrental.models import Car, Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ('car',
                    'customer_name',
                    'customer_phone',
                    'customer_email',
                    'booking_start',
                    'booking_end',
                    'booking_message',
                    'is_approved'
                    )
    list_filter = ['is_approved']
    search_fields = ['customer_name',
                     'customer_phone',
                     'customer_email']
    list_editable = ['is_approved']
    actions = ['email_customer']

    def email_customer(self, request, queryset):
        for booking in queryset:
            if booking.is_approved:
                email_body = """Dear {}: 
                We are pleased to inform you that your booking has been approved.
                Thinks.
                """.format(booking.customer_name)
            else:
                email_body = """Dear {}:
                Unfortunately we do not have the capacity right now to accept your booking.
                Thinks.
                """.format(booking.customer_name)
            print(email_body)
            self.message_user(request, "Email were send successfully")
    email_customer.short_description = "Sending email about booking status."


admin.site.register(Booking, BookingAdmin)
admin.site.register(Car)