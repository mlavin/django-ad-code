try:
    from django.apps import AppConfig
except ImportError:
    AppConfig = object
 

class AdCodeConfig(AppConfig):
    name = 'adcode'

    def ready(self):
        from . import recievers
