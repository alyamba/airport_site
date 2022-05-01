import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy

from .models import *
from .urls import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin

# menu = [{'title': 'О сайте', 'url_name': 'about'},
#         {'title': 'Купить билет', 'url_name': 'buy_ticket'},
#         ]


class FlightHome(DataMixin, ListView):
    model = Flight
    template_name = 'airport/index.html'
    context_object_name = 'next_airport_flights'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['menu'] = menu
        # context['title'] = 'Главная страница'
        c_def = self.get_user_context(title='Главная страница')
        # context = dict(list(context.items())+list(c_def.items()))
        return context | c_def

    def get_queryset(self):
        return Flight.objects.order_by('departure_time')[:5]


def flight_detail(request, flight_slug):
    flight = get_object_or_404(Flight, slug=flight_slug)
    # print('FLIGHT:', flight_slug)
    # try:
    #     a = Flight.objects.get(slug=flight_slug)
    # except:
    #     raise Http404("Рейс не найден")
    context = {
        'flight': flight,
        'menu': menu,
        'title': flight.route,
    }
    return render(request, 'airport/flight_details.html', context=context)


def error_404(request, exception):
    return HttpResponseNotFound('Страница не найдена')


def register(request):
    hi = 'hi'
    return HttpResponse(hi)


def about(request):
    context = {
        'menu': menu,
    }
    return render(request, 'airport/about.html', context=context)
    # return HttpResponse('О сайте')


class BuyTicket(LoginRequiredMixin, DataMixin, CreateView):
    form_class = BuyTicketForm
    template_name = 'airport/buy_ticket.html'
    success_url = reverse_lazy('airport:home')
    login_url = reverse_lazy('airport:home')  #если не авторизован, перенаправляет по ссылке

    # BuyTicketForm.data.ticket_time_buy = datetime.datetime.now()
    # BuyTicketForm.data.save()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Купить билет')
        return context | c_def


    # def form_valid(self, request, form):
    #     if request.method == "POST":
    #         form = BuyTicketForm(request.POST)
    #         if form.is_valid():
    #             data = form.save(commit=False)
    #             data.ticket_time_buy = datetime.datetime.now()
    #             data.save()
    #             return redirect('/airport/')
    #     else:
    #         form = BuyTicketForm()
    #     return render(request, 'airport/buy_ticket.html', {'form': form})

# def buy_ticket(request):
#     if request.method == "POST":
#         form = BuyTicketForm(request.POST)
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.ticket_time_buy = datetime.datetime.now()
#             data.save()
#             return redirect('/airport/')
#     else:
#         form = BuyTicketForm()
#     return render(request, 'airport/buy_ticket.html', {'form': form, 'menu': menu, 'title': 'Купить билет'})


def login(request):
    return HttpResponse('Войти')


# class RegisterUser(DataMixin, CreateView):
#     form_class = UserCreateForm
#     template_name = 'airport/register.html'
#     success_url = reserve_lazy('login')