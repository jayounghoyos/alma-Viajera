from django.contrib import admin
from .models import Categoria, Item

# Inline for Item inside Categoria
class ItemInline(admin.TabularInline):
    model = Item
    extra = 1  # Number of empty forms to show
    autocomplete_fields = ['categoria'] 
    fields = ('nombre', 'descripcion', 'precio', 'ubicacion', 'disponibilidad', 'stock', 'imagenes')
    verbose_name = "Item"
    verbose_name_plural = "Items"

# Categoria admin
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    inlines = [ItemInline]
    search_fields = ['nombre', 'descripcion']

# Optional: also register Item standalone
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'disponibilidad', 'stock')
    list_filter = ('categoria', 'disponibilidad')
    search_fields = ['nombre', 'descripcion', 'categoria__nombre']
    autocomplete_fields = ['categoria']
