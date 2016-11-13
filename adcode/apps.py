from django.apps import AppConfig


class AdCodeConfig(AppConfig):
    name = 'adcode'

    def ready(self):
        from . import recievers  # noqa
