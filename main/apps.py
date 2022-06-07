from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'


class DashboardConfig(AppConfig):
    verbose_name = 'Modules Management'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'