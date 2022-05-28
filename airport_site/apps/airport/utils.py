from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Аналитика', 'url_name': 'analytics'},
        {'title': 'Оценка', 'url_name': 'expert_opinion'},
        {'title': 'Купить билет', 'url_name': 'buy_ticket'},
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
            context = kwargs

            user_menu = menu.copy()
            if not self.request.user.is_authenticated:
                del user_menu[2:4]

            context['menu'] = user_menu
            return context