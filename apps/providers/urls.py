from django.urls import path
from .views import DashboardView, crear_servicio, VerServiciosView, EditarServicioView, EliminarServicioView, eliminar_servicio_ajax

app_name = "providers"

urlpatterns = [
    path("account/", DashboardView.as_view(), name="dashboard"),
    path('crear-servicio/', crear_servicio, name='crear_servicio'),
    path('mis-servicios/', VerServiciosView.as_view(), name='ver_servicios'),
    path('editar-servicio/<int:pk>/', EditarServicioView.as_view(), name='editar_servicio'),
    path('eliminar-servicio/<int:pk>/', EliminarServicioView.as_view(), name='eliminar_servicio'),
    path('eliminar-servicio-ajax/<int:pk>/', eliminar_servicio_ajax, name='eliminar_servicio_ajax'),
]
