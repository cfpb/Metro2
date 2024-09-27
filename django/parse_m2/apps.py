from django.apps import AppConfig


class ParseM2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parse_m2'
    verbose_name='Parse M2'

    # Override built-in ready() method to ensure task scheduler is started
    #   exactly once when the application starts up
    def ready(self):
        from users import task

        task.start()

        return super().ready()