from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # AbstractUser already has: username, email, password, first_name, last_name, etc.
    telefono = models.CharField(max_length=20, blank=True, null=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    es_proveedor = models.BooleanField(default=False)


class UsuarioFinal(Usuario):
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.direccion}"


class UsuarioVendedor(Usuario):
    descripcion = models.TextField(blank=True, null=True)
