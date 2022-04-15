from django.urls import path, re_path

from .views import *

app_name = 'airport'

urlpatterns = [
    path('', FlightHome.as_view(), name='home'),
    path('<int:flight_id>', flight_detail, name='flight_detail'),
    path('register/', register, name='register'),
    path('about/', about, name='about'),
    path('buy_ticket/', buy_ticket, name='buy_ticket'),
    path('login/', login, name='login'),
]
