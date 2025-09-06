from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path("providers/", include(("apps.providers.urls", "providers"), namespace="providers")),
    path('', include('apps.catalog.urls')),
    path('carrito/', include('apps.cart.urls')),
    path('users/', include('apps.user.urls')),  # Include the users app URLs
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)