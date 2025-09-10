from django.db import models
from django.conf import settings
#from apps.user.models import UsuarioVendedor
from django.views.generic import DetailView


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

    def promedio_calificacion(self):
        calificaciones = self.calificaciones.all()
        if calificaciones.exists():
            return round(sum(c.puntuacion for c in calificaciones) / calificaciones.count(), 2)
        return 0

    def estrellas(self):
        promedio = self.promedio_calificacion() or 0
        llenas = int(promedio)
        media = 1 if (promedio - llenas) >= 0.5 else 0
        vacias = 5 - llenas - media
        return {"llenas": llenas, "media": media, "vacias": vacias}


class ItemDetailView(DetailView):
    model = Item
    template_name = 'catalog/item_detail.html'
    context_object_name = 'item'


class Calificacion(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name="calificaciones")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    puntuacion = models.PositiveSmallIntegerField()  # Valor entre 1 y 5
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('item', 'usuario')

    def __str__(self):
        return f"{self.usuario} - {self.item} ({self.puntuacion})"
