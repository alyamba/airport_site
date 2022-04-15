import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *
from .urls import *
from .forms import *
from django.views.generic import ListView, DetailView

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Купить билет', 'url_name': 'buy_ticket'},
        {'title': 'Войти', 'url_name': 'login'}
        ]


class FlightHome(ListView):
    model = Flight
    template_name = 'airport/index.html'
    context_object_name = 'next_airport_flights'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Flight.objects.order_by('departure_time')[:5]


# def index(request):
#     next_airport_flights = Flight.objects.order_by('-departure_time')[:5]
#
#     context = {
#         'next_airport_flights': next_airport_flights,
#         'title': 'Главная страница',
#         'menu': menu,
#     }
#     return render(request, 'airport/index.html', context=context)


def flight_detail(request, flight_id):
    print('FLIGHT:', flight_id)
    try:
        a = Flight.objects.get(id=flight_id)
    except:
        raise Http404("Рейс не найден")

    context = {
        'flight': a,
        'menu': menu,
    }
    return render(request, 'airport/flight_details.html', context=context)


def error_404(request, exception):
    return HttpResponseNotFound('Страница не найдена')


def register(request):
    hi = 'hi'
    return HttpResponse(hi)


def about(request):
    return render(request, 'airport/about.html')
    # return HttpResponse('О сайте')


def buy_ticket(request):
    if request.method == "POST":
        form = BuyTicketForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            # TODO: add time to this field
            data.ticket_time_buy = datetime.date.today()
            data.save()
            return redirect('/airport/')
    else:
        form = BuyTicketForm()
    return render(request, 'airport/buy_ticket.html', {'form': form, 'menu': menu, 'title': 'Купить билет'})


def login(request):
    return HttpResponse('Войти')
