from django.db import models
from django.conf import settings
#from apps.user.models import UsuarioVendedor
from django.views.generic import DetailView

# Create your models here.
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)  
    nombre = models.CharField(
        max_length=50,
        choices=[
            ('lugar', 'Lugar'),
            ('tour', 'Tour'),
            ('comida', 'Comida'),
            ('souvenir', 'Souvenir'),
            ('actividad', 'Actividad'),
        ]
    )
    descripcion = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.nombre

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    #usuario = models.ForeignKey(UsuarioVendedor, on_delete=models.CASCADE, related_name="items")
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="items")
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.ImageField(upload_to="items/", blank=True, null=True)
    tiempo = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    disponibilidad = models.BooleanField(default=True)  # tours/actividades
    stock = models.PositiveIntegerField(blank=True, null=True)  # souvenirs

    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,          # modelo de usuario
        on_delete=models.CASCADE,
        related_name="items_publicados",   
    )
    def __str__(self):
        return f"{self.nombre} ({self.categoria})"


class ItemDetailView(DetailView):
    """Vista genérica para mostrar los detalles de un producto."""
    model = Item
    template_name = 'catalog/item_detail.html'
    context_object_name = 'item'