from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

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


class RegisterUserForm(UserCreationForm):
    user_surname = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    user_name = forms.CharField(label='Имя',  widget=forms.TextInput(attrs={'class': 'form-input'}))
    user_patronymic = forms.CharField(label='Отчество',  widget=forms.TextInput(attrs={'class': 'form-input'}))
    user_mail = forms.EmailField(label='Электронная почта',  widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('user_surname', 'user_name', 'user_patronymic', 'user_mail', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    user_mail = forms.EmailField(label='Электронная почта',  widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
