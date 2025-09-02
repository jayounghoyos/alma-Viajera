from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.user.models import UsuarioFinal
from apps.catalog.models import Item

class Reserva(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", _("Pendiente")
        CONFIRMADA = "confirmada", _("Confirmada")
        CANCELADA = "cancelada", _("Cancelada")

    usuario = models.ForeignKey(
        UsuarioFinal,
        on_delete=models.CASCADE,
        related_name="reservas"
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="reservas"
    )
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    cantidad = models.PositiveIntegerField(default=1)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )
    pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f"Reserva {self.id} - {self.usuario_final.nombre} - {self.estado}"

class Pago(models.Model):
    METODOS_PAGO = [
        ("tarjeta", "Tarjeta de Crédito/Débito"),
        ("paypal", "PayPal"),
        ("transferencia", "Transferencia Bancaria"),
    ]

    ESTADOS_PAGO = [
        ("pendiente", "Pendiente"),
        ("completado", "Completado"),
        ("fallido", "Fallido"),
    ]

    id = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=20, choices=METODOS_PAGO)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_PAGO, default="pendiente")
    transaccion_id = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return f"Pago {self.id} - {self.metodo} - {self.estado}"

class Factura(models.Model):
    usuario = models.ForeignKey(UsuarioFinal, on_delete=models.CASCADE, related_name="facturas")
    fecha_emision = models.DateTimeField(auto_now_add=True)
    reserva = models.ForeignKey("Reserva", on_delete=models.CASCADE, related_name="factura")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Factura {self.id} - Usuario {self.usuario_final.username}"