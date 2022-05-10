from django.contrib import admin

from .models import *
from django.contrib.auth.models import User


class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'departure_city', 'arrival_city', 'departure_time', 'arrival_time')
    list_display_links = ('departure_city', 'arrival_city',)
    search_fields = ('departure_city', 'arrival_city',)
    list_filter = ('departure_time', )
    prepopulated_fields = {"slug": ("departure_city", "arrival_city")}


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'flight', 'user', 'ticket_time_buy')
    list_display_links = ('id', 'flight', 'user')
    search_fields = ('flight',)
    list_filter = ('user',)


admin.site.register(Flight, FlightAdmin)
admin.site.register(Ticket, TicketAdmin)

