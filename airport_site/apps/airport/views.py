from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *
from .urls import *
from .forms import *


menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Купить билет', 'url_name': 'buy_ticket'},
        {'title': 'Войти', 'url_name': 'login'}
]

def index(request):
    next_airport_flights = Flight.objects.order_by('-departure_time')[:5]

    for m in menu:
        a = m.get('url_name')
        print(a)


    context = {
        'next_airport_flights': next_airport_flights,
        'title': 'Главная страница',
        'menu': menu,
        'a': a
    }
    return render(request, 'airport/index.html', context=context)

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

def about(request):
    return HttpResponse('О сайте')

def buy_ticket(request):
    if request.method == "POST":
        form = BuyTicketForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return redirect('/airport/')
    else:
        form = BuyTicketForm()
    return render(request, 'airport/buy_ticket.html', {'form': form, 'menu': menu, 'title': 'Купить билет'})

def login(request):
    return HttpResponse('Войти')
