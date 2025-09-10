from django.db import models
from apps.catalog.models import Item
from apps.user.models import Usuario  # Cambiar de UsuarioFinal a Usuario

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"  # Cambiado a 'self.usuario_id.username'

    def calcular_total(self):
        total = sum(
            item.cantidad * item.item.precio for item in self.items.all()
        )
        self.total = total
        self.save()
        return self.total
class CarritoItem(models.Model):
    carrito = models.ForeignKey(  # Cambiado de 'carrito_id' a 'carrito'
        Carrito,
        related_name="items",
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Cambiado de 'item_id' a 'item'
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.item.nombre}"  # Asegúrate de que 'Item' tiene 'nombre'

    @property
    def subtotal(self):
        return self.cantidad * self.item.precio
