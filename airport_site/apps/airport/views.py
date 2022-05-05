import datetime

from django.contrib.auth import logout
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



def about(request):
    context = {
        'menu': menu,
    }
    return render(request, 'airport/about.html', context=context)


class BuyTicket(LoginRequiredMixin, DataMixin, CreateView):
    form_class = BuyTicketForm
    template_name = 'airport/buy_ticket.html'
    success_url = reverse_lazy('airport:home')
    login_url = reverse_lazy('airport:home')  #если не авторизован, перенаправляет по ссылке

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Купить билет')
        return context | c_def


# def login(request):
#     return HttpResponse('Войти')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'airport/register.html'
    success_url = reverse_lazy('airport:login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context | c_def


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
    return redirect('airport:login')
