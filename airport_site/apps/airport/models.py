from django.db import models

class Flight(models.Model):
    route = models.CharField('Название рейса', max_length=30)
    departure_time = models.DateTimeField('Дата и время рейса')

    def __str__(self):
        return self.route + ' | ' + str(self.departure_time)

    class Meta:
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ['route']


class User(models.Model):
    user_surname = models.CharField('Фамилия', max_length=25)
    user_name = models.CharField('Имя', max_length=25)
    user_patronymic = models.CharField('Отчество', max_length=25)
    user_mail = models.EmailField('Электронная почта', max_length=50)

    def __str__(self):
        return self.user_surname + " " + self.user_name + " " + self.user_mail

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['user_surname']


class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_time_buy = models.DateTimeField('Время покупки')

    def __str__(self):
        return self.user.user_mail + ' | ' + self.flight.route + ' | ' + str(self.ticket_time_buy)

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'

