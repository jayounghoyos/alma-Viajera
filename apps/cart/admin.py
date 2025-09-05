from django.contrib import admin
from .models import Carrito, CarritoItem

# Inline for CarritoItem inside Carrito
class CarritoItemInline(admin.TabularInline):
    model = CarritoItem
    extra = 1  # Number of empty forms to show
    autocomplete_fields = ['item_id'] 
    verbose_name = "Item del carrito"
    verbose_name_plural = "Items del carrito"

# Carrito admin
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario_id', 'total')
    inlines = [CarritoItemInline]
    search_fields = ['usuario_id__username', 'usuario_id__nombre']
    readonly_fields = ['total']  # Total will be calculated

# Optional: also register CarritoItem standalone
@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('carrito_id', 'item_id', 'cantidad')
    search_fields = ['carrito_id__usuario_id__username', 'item_id__nombre']
