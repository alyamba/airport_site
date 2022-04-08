from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

def index(request):
    return HttpResponse('Страница приложения')

def flights(request, flight_id):
    return HttpResponse('Страница с маршрутами')

def error_404(request, exception):
    return HttpResponseNotFound('Страница не найдена')
