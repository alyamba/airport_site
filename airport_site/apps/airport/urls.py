from django.urls import path

from .views import *

app_name = 'airport'

urlpatterns = [
    path('', index, name='home'),
    path('<int:flight_id>', flight_detail, name='flight_detail'),
    path('register/', register, name='register'),
]
