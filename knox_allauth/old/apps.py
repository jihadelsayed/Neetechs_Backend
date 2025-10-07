from django.apps import AppConfig


class KnoxAllauthConfig(AppConfig):
    name = 'knox_allauth'
    def ready(self):
    	import knox_allauth.signals
