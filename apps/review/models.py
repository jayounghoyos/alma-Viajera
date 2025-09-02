from django.db import models
from apps.catalog.models import Item
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-fecha']
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        return f'Reseña de {self.usuario_final.username} ({self.puntuacion} estrellas)'

