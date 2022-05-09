from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Flight(models.Model):
    route = models.CharField('Название рейса', max_length=30)
    departure_time = models.DateTimeField('Дата и время вылета')
    route_info = models.TextField('Информация о рейсе')
    arrival_time = models.DateTimeField('Дата и время рейса прилёта')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.route + ' | ' + str(self.departure_time)

    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ['route']

    def get_absolute_url(self):
        return reverse('flight', kwargs={'flight_slug': self.slug})


class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_time_buy = models.DateTimeField('Время покупки', auto_now_add=True)

    def __str__(self):
        return self.user.username + ' | ' + self.flight.route + ' | ' + str(self.ticket_time_buy)

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
