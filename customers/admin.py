from django.contrib import admin
from .models import *

admin.site.register(Customer)



class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'bike', 'rent_start_date', 'rent_end_date', 'status', 'created_at')
    list_filter = ('status',)
    actions = ['accept_booking', 'reject_booking']

    def accept_booking(self, request, queryset):
        queryset.update(status='accepted')
        self.message_user(request, "Selected bookings have been accepted.")

    def reject_booking(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Selected bookings have been rejected.")

    accept_booking.short_description = "Accept selected bookings"
    reject_booking.short_description = "Reject selected bookings"


admin.site.register(Bike)
admin.site.register(Booking, BookingAdmin)