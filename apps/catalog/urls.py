from django.urls import path
from django.views.generic import TemplateView
from .views import CatalogView

from django.conf import settings
from django.conf.urls.static import static

app_name = "catalog"

urlpatterns = [
    path("catalog/", CatalogView.as_view(), name="catalog"),
    #path("catalog/", TemplateView.as_view(template_name="catalog.html"), name="catalog"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)