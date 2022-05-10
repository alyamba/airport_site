from django.urls import path, re_path

from .views import *

app_name = 'airport'


urlpatterns = [
    path('', FlightHome.as_view(), name='home'),
    path('flight/<slug:flight_slug>/', flight_detail, name='flight_detail'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('about/', about, name='about'),
    path('buy_ticket/', BuyTicket.as_view(), name='buy_ticket'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('tickets/', Tickets.as_view(), name='tickets')
]
