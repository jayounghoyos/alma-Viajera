from django.db import models

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
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="items")
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    imagenes = models.ImageField(upload_to="items/", blank=True, null=True)
    disponibilidad = models.BooleanField(default=True)  # tours/actividades
    stock = models.PositiveIntegerField(blank=True, null=True)  # souvenirs
    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
