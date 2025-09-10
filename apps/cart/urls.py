from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.carrito_view, name='detalle'),
    path('agregar/<int:item_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('incrementar/<int:item_id>/', views.incrementar_cantidad, name='incrementar_cantidad'),
    path('decrementar/<int:item_id>/', views.decrementar_cantidad, name='decrementar_cantidad'),
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar'),
    path('requiere-inicio-sesion/', views.requiere_inicio_sesion, name='requiere_inicio_sesion'),
]