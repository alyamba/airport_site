from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Купить билет', 'url_name': 'buy_ticket'},
        {'title': 'Войти', 'url_name': 'login'}
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
            context = kwargs
            context['menu'] = menu
            return context