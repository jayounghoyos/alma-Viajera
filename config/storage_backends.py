from storages.backends.gcloud import GoogleCloudStorage
from django.conf import settings

class MediaRootGoogleCloudStorage(GoogleCloudStorage):
    """Almacenamiento para archivos subidos por el usuario (MEDIA)."""
    location = "media"
    file_overwrite = False
