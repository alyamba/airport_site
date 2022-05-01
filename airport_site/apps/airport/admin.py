from django.contrib import admin

from .models import *

class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'departure_time')
    list_display_links = ('route', )
    search_fields = ('route', )
    list_filter = ('departure_time', 'route')
    prepopulated_fields = {"slug": ("route", )}

# class TicketAdmin(admin.ModelAdmin):
#     list_display = ('id', 'Flight.route')
#     list_display_links = ('id', )
#     search_fields = ('route', )


admin.site.register(Flight, FlightAdmin)
admin.site.register(User)
admin.site.register(Ticket)

