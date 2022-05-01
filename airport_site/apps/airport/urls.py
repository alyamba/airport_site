from django.urls import path, re_path

from .views import *

app_name = 'airport'

urlpatterns = [
    path('', FlightHome.as_view(), name='home'),
    path('flight/<slug:flight_slug>/', flight_detail, name='flight_detail'),
    path('register/', register, name='register'),
    path('about/', about, name='about'),
    path('buy_ticket/', BuyTicket.as_view(), name='buy_ticket'),
    path('login/', login, name='login'),
]
