from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *


menu = ["О сайте", "Купить билет", "Войти"]

def index(request):
    next_airport_flights = Flight.objects.order_by('-departure_time')[:5]
    return render(request, 'airport/index.html', {'next_airport_flights': next_airport_flights, 'title': 'Главная страница', 'menu': menu})

def flight_detail(request, flight_id):
    try:
        a = Flight.objects.get(id=flight_id)
    except:
        raise Http404("Рейс не найден")
    return render(request, '', {'flight': a})

def error_404(request, exception):
    return HttpResponseNotFound('Страница не найдена')

def register(request):
    hi = 'hi'
    return HttpResponse(hi)

