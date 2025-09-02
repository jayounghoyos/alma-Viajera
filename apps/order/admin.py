from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Reserva, Pago, Factura


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "item", "fecha_reserva", "cantidad", "estado", "pago")
    list_filter = ("estado", "fecha_reserva")
    search_fields = ("usuario_final__nombre", "item__nombre")
    ordering = ("-fecha_reserva",)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id", "monto", "metodo", "fecha_pago", "estado", "transaccion_id")
    list_filter = ("metodo", "estado")
    search_fields = ("transaccion_id",)
    ordering = ("-fecha_pago",)


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "reserva", "fecha_emision", "monto_total")
    list_filter = ("fecha_emision",)
    search_fields = ("usuario__nombre", "reserva__id")
    ordering = ("-fecha_emision",)
