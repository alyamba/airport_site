from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from datetime import datetime
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class Flight(models.Model):
    departure_city = models.CharField('Город вылета', max_length=30)
    arrival_city = models.CharField('Город прилёта', max_length=30)
    departure_time = models.DateTimeField('Дата и время вылета')
    arrival_time = models.DateTimeField('Дата и время рейса прилёта')
    route_info = models.TextField('Информация о рейсе')
    price = models.DecimalField('Цена билета', max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.departure_city + '-' + self.arrival_city + ' | ' + str(self.departure_time.strftime("%d %B %Y в %H:%M")) + ' | ' + str(self.arrival_time.strftime("%d %B %Y в %H:%M"))

    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ['departure_city', 'arrival_city']

    def get_absolute_url(self):
        return reverse('flight', kwargs={'flight_slug': self.slug})


class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='flights')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets') #stop in this place https://stackoverflow.com/questions/34184046/how-to-get-all-objects-referenced-as-foreignkey-from-given-field-in-a-module-in
    ticket_time_buy = models.DateTimeField('Время покупки', auto_now_add=True)

    def __str__(self):
        info = self.user.username + ' | ' + self.flight.departure_city + '-' + self.flight.arrival_city \
               + ' | ' + str(self.flight.departure_time.strftime("%d %B %Y в %H:%M"))\
               + ' | ' + str(self.flight.arrival_time.strftime("%d %B %Y в %H:%M"))\
               + ' | ' + str(self.ticket_time_buy.strftime("%d %B %Y в %H:%M"))
        return info

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'

#TODO: добавить экспертов