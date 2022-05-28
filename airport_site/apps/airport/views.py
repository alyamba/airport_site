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
from django.db.models import Avg, Count, Min, Sum


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
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        del user_menu[2:4]

    context = {
        'flight': flight,
        'menu': user_menu,
        'title': flight.departure_city + '-' + flight.arrival_city,
    }
    return render(request, 'airport/flight_details.html', context=context)


def error_404(request, exception):
    return HttpResponseNotFound('Страница не найдена')


def about(request):
    # TODO: добавить информацию о сайте
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        del user_menu[2:4]
    context = {
        'menu': user_menu,
        'title': "О сайте",
    }
    return render(request, 'airport/about.html', context=context)


def buy_ticket(request):
    if request.method == 'POST':
        form = BuyTicketForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('airport:home')
            except:
                form.add_error(None, 'Ошибка добавления')
    else:
        form = BuyTicketForm(initial={'user': request.user.pk})
    context = {
        'form': form,
        'menu': menu,
        'title': "Купить билет"
    }
    return render(request, 'airport/buy_ticket.html', context=context)

# class BuyTicket(DataMixin, CreateView):
#     form_class = BuyTicketForm
#     user = User.objects.get(pk=2)
#     print(user.pk)
#     template_name = 'airport/buy_ticket.html'
#     success_url = reverse_lazy('airport:home')
#
#     # TODO: автоматическое добавление авторизированного пользователя в покупку билета
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         self.form_class(initial={'user': 2})
#         print(self.request.user.pk)
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Купить билет')
#         user = self.get_user_context(title='user')
#         return context | c_def | user


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
        user_id = self.request.user
        tickets = Ticket.objects.filter(user=user_id)
        context['tickets'] = tickets
        return context | c_def

    def get_queryset(self):
        user_id = self.request.user
        return user_id.tickets.all()
    # TODO: корректный вывод всех билетов


def expert_opinion(request):
    if request.method == 'POST':
        form = ExpertForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('airport:home')
            except:
                form.add_error(None, 'Ошибка добавления')
        else:
            context = {
                'form': form,
                'menu': menu,
                'title': "Оценка работы аэропорта"
            }
            return render(request, 'airport/error.html', context=context)
    else:
        form = ExpertForm(initial={'user': request.user.pk})
    context = {
        'form': form,
        'menu': menu,
        'title': "Оценка работы аэропорта"
    }
    return render(request, 'airport/expert.html', context=context)


def analytics(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        del user_menu[2:4]

    # Количество записей
    count = Expert.objects.count()

    # Определяется сумма рангов всех экспертов по каждому фактору
    sum1 = Expert.objects.values().aggregate(Sum('factor1'))['factor1__sum']
    sum2 = Expert.objects.values().aggregate(Sum('factor2'))['factor2__sum']
    sum3 = Expert.objects.values().aggregate(Sum('factor3'))['factor3__sum']
    sum4 = Expert.objects.values().aggregate(Sum('factor4'))['factor4__sum']
    sum5 = Expert.objects.values().aggregate(Sum('factor5'))['factor5__sum']

    # Вычисляется общая сумма рангов всех экспертов
    full_sum = sum1 + sum2 + sum3 + sum4 + sum5

    # Вычисляется средняя сумма рангов
    mean_sum = full_sum/5

    # Определяется отклонение суммы рангов каждого фактора от средней суммы рангов
    deviation_sum1 = sum1 - mean_sum
    deviation_sum2 = sum2 - mean_sum
    deviation_sum3 = sum3 - mean_sum
    deviation_sum4 = sum4 - mean_sum
    deviation_sum5 = sum5 - mean_sum

    # Степень согласованности мнений экспертов оценивается с помощью коэффициента конкордации
    degree_consistency = (12*(deviation_sum1**2+deviation_sum2**2+deviation_sum3**2+deviation_sum4**2+deviation_sum5**2)/(count**2*(5**3-5)))
    print('Степень согласованности', degree_consistency)

    if degree_consistency <= 0.5:
        information = 'Низкая согласованность экспертных оценок'
    else:
        k = degree_consistency * count * 4
        information = 'Коэффициент Пирсона табличное и полученное: 7,81 и ' + str(k)

    array = [{'name': 'Цена билета', 'value': sum1, 'index': 1},
             {'name': 'Качество перелета', 'value': sum2, 'index': 2},
             {'name': 'Состояние самолёта', 'value': sum3, 'index': 3},
             {'name': 'Разнообразие рейсов', 'value': sum4, 'index': 4},
             {'name': 'Работа сайта', 'value': sum5, 'index': 5},
             ]

    sort = sorted(array, key=lambda d: d['value'])

    name = []
    value = []
    for i in sort:
        name.append(i['name'])
        value.append(i['value'])
    print(name)
    print(value)

   # Определяется удельный вес фактора
    index = 0
    specific_graviry1 = 0
    for factor in sort:
        if factor['index'] == 1:
            specific_graviry1 = 2 * (5 - (index + 1) + 1)/(5 * (5 + 1))
        else:
            index = index + 1

    index = 0
    specific_graviry2 = 0
    for factor in sort:
        if factor['index'] == 2:
            specific_graviry2 = 2 * (5 - (index + 1) + 1) / (5 * (5 + 1))
        else:
            index = index + 1

    index = 0
    specific_graviry3 = 0
    for factor in sort:
        if factor['index'] == 3:
            specific_graviry3 = 2*(5-(index+1)+1)/(5*(5+1))
        else:
            index = index + 1

    index = 0
    specific_graviry4 = 0
    for factor in sort:
        if factor['index'] == 4:
            specific_graviry4 = 2*(5-(index+1)+1)/(5*(5+1))
        else:
            index = index + 1

    index = 0
    specific_graviry5 = 0
    for factor in sort:
        if factor['index'] == 5:
            specific_graviry5 = 2 * (5 - (index + 1) + 1) / (5 * (5 + 1))
        else:
            index = index + 1

    array_new = [{'name': 'Цена билета', 'value': specific_graviry1, 'index': 1},
             {'name': 'Качество перелета', 'value': specific_graviry2, 'index': 2},
             {'name': 'Состояние самолёта', 'value': specific_graviry3, 'index': 3},
             {'name': 'Разнообразие рейсов', 'value': specific_graviry4, 'index': 4},
             {'name': 'Работа сайта', 'value': specific_graviry5, 'index': 5},
             ]
    sort_new = sorted(array_new, key=lambda d: d['value'])

    name_new = []
    value_new = []
    for i in sort_new:
        name_new.append(i['name'])
        value_new.append(i['value'])

    context = {
        'menu': user_menu,
        'title': "Аналитика",
        'labels': name_new,
        'data': value_new,
        'information': information,
    }

    return render(request, 'airport/analytics.html', context=context)


