# carrito/models.py
from django.db import models
from apps.catalog.models import Item 
from apps.user.models import UsuarioFinal 

class Carrito(models.Model):
    usuario_id = models.ForeignKey(UsuarioFinal, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Carrito de {self.usuario.nombre}"
    
    def calcular_total(self):
        total = sum(
            item.cantidad * item.item.precio for item in self.items.all()
        )
        self.total = total
        self.save()
        return self.total
    
class CarritoItem(models.Model):
    carrito_id = models.ForeignKey(
        Carrito,
        related_name="items", 
        on_delete=models.CASCADE
    )
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.item.nombre}"
