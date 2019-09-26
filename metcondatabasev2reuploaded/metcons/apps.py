from django.apps import AppConfig


class MetconsConfig(AppConfig):
    name = 'metcons'

    def ready(self):
        import update
        update.start()
