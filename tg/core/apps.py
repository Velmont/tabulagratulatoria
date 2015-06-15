import autocomplete_light
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        autocomplete_light.register(
            self.get_model('Postnummer'),
            search_fields=('postnr', 'poststad'),
        )
