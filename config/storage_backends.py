from storages.backends.gcloud import GoogleCloudStorage
from google.auth import default

class MediaRootGoogleCloudStorage(GoogleCloudStorage):
    """Almacenamiento para archivos subidos por el usuario (MEDIA)."""
    bucket_name = "alma-viajera-media"
    location = "media"
    file_overwrite = False
    default_acl = None

    def __init__(self, *args, **kwargs):
        # Usa las credenciales predeterminadas del entorno (Cloud Run)
        credentials, project_id = default()
        kwargs['credentials'] = credentials
        kwargs['project'] = project_id
        super().__init__(*args, **kwargs)
