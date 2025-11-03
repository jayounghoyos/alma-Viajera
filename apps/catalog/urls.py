from django.urls import path
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static
from .views import CatalogView, ItemDetailView, MapView, item_detail_api, items_list_api

app_name = "catalog"

urlpatterns = [
    path("mapa/", MapView.as_view(), name="mapa"),
    path("explorar/<str:place>/<str:categoria>", CatalogView.as_view(), name="explorar"),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('api/items/', items_list_api, name='items_list_api'),
    path('api/item/<int:id>/', item_detail_api, name='item_detail_api'),
]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)