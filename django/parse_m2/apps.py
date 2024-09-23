from django.apps import AppConfig


class ParseM2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parse_m2'
    verbose_name='Parse M2'

    def ready(self):
        from users import task
        
        task.start()