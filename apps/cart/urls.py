from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.carrito_view, name='detalle'),  # Ruta para /carrito/
]