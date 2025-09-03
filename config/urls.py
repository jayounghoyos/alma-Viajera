from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas de autenticación y registro (aparecen en /login, /logout, /signup, /providers/signup)
    path('', include(('apps.user.urls', 'users'), namespace='users')),


    # Core (home y about)
    path('', include(('apps.core.urls', 'core'), namespace='core')),
    
    # Rutas propias de proveedores bajo /providers/...
    path('providers/', include(('apps.providers.urls', 'providers'), namespace='providers')),

    path('', include('apps.core.urls')),
    path("", include("apps.listings.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)