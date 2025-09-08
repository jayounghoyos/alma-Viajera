from django.urls import path
from .views import DashboardView, crear_servicio

app_name = "providers"

urlpatterns = [
    path("account/", DashboardView.as_view(), name="dashboard"),
    path('crear-servicio/', crear_servicio, name='crear_servicio'),
]
