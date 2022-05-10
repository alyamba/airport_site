import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy

from .models import *
from .urls import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin


class FlightHome(DataMixin, ListView):
    model = Flight
    template_name = 'airport/index.html'
    context_object_name = 'next_airport_flights'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return context | c_def

    def get_queryset(self):
        return Flight.objects.order_by('departure_time')[:5]


def flight_detail(request, flight_slug):
    #TODO: вывод всех данных о рейсе
    flight = get_object_or_404(Flight, slug=flight_slug)
    context = {
        'flight': flight,
        'menu': menu,
        'title': flight.departure_city + '-' + flight.arrival_city,
    }
    return render(request, 'airport/flight_details.html', context=context)


def error_404(request, exception):
    return HttpResponseNotFound('Страница не найдена')


def about(request):
    # TODO: добавить информацию о сайте
    context = {
        'menu': menu,
    }
    return render(request, 'airport/about.html', context=context)


class BuyTicket(DataMixin, CreateView):
    form_class = BuyTicketForm
    template_name = 'airport/buy_ticket.html'
    success_url = reverse_lazy('airport:home')

    # TODO: корректное добавление билетов с сайта
    # TODO: автоматическое добавление авторизированного пользователя в покупку билета
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Купить билет')
        return context | c_def


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'airport/register.html'
    success_url = reverse_lazy('airport:login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context | c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('airport:home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'airport/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('airport:home')


def logout_user(request):
    logout(request)
    return redirect('airport:home')


class Tickets(DataMixin, ListView):
    model = Ticket
    template_name = 'airport/tickets.html'
    context_object_name = 'my_ticket'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Ваши билеты')
        return context | c_def

    def get_queryset(self):
        user_id = self.request.user
        ticket = Ticket.objects.filter(user=user_id)
        print(user_id.tickets.all())
        print('*************************')
        print(Flight.objects.filter())
        return user_id.tickets.all()
    # TODO: корректный вывод всех билетов