from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('flights/<int:flight_id>', flights, name='flight_id'),
]