from django import forms
from .models import *


class BuyTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['flight'].empty_label = "Рейс не выбран"
        self.fields['user'].empty_label = "Пассажир не выбран"
        self.fields['flight'].label = "Рейс"
        self.fields['user'].label = "Пассажир"
        # self.fields['ticket_time_buy'].label = "Время покупки"
        # self.ticket_time_buy = timezome.now()

    class Meta:
        model = Ticket
        fields = ['flight', 'user']

