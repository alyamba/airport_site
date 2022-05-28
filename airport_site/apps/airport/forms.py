from urllib import request

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import TextInput


class BuyTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['flight'].empty_label = "Рейс не выбран"
        self.fields['user'].empty_label = "Пользователь не выбран"
        self.fields['flight'].label = "Рейс"
        self.fields['user'].label = "Пассажир"

    class Meta:
        model = Ticket
        fields = ['flight', 'user']

        widgets = {
        }


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Фамилия'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повтор пароля'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))


class ExpertForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['factor1'].label = "Цена билета"
        self.fields['factor2'].label = "Качество перелета"
        self.fields['factor3'].label = "Состояние самолёта"
        self.fields['factor4'].label = "Разнообразие рейсов"
        self.fields['factor5'].label = "Работа сайта"

    class Meta:
        model = Expert
        fields = ['factor1', 'factor2', 'factor3', 'factor4', 'factor5', 'user']

