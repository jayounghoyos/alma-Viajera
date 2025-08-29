from django.apps import AppConfig

class ListingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.listings'      # ← IMPORTANTE: paquete completo
    verbose_name = 'Catálogo'
