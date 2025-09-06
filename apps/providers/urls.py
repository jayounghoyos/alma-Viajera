from django.urls import path
from . import views
from .views import DashboardView, dashboard

app_name = "providers"

urlpatterns = [
    path("account/", views.dashboard, name="dashboard"),
]
