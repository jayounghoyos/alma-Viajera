# Juan Andrés Young Hoyos
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "core"

urlpatterns = [
    path("", TemplateView.as_view(template_name="core/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="core/about.html"), name="about"),
    path("qr-reservation/", views.qr_reservation, name="qr_reservation"),
    path("qr/export/", views.export_qr, name="export_qr"),
    path("qr/<int:reservation_id>/export/", views.export_qr, name="export_qr_with_id"),
]
