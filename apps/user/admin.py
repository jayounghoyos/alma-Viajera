from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UsuarioFinal, UsuarioVendedor

@admin.register(UsuarioFinal)
class UsuarioFinalAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "direccion", "es_proveedor")
    search_fields = ("username", "email", "direccion")

@admin.register(UsuarioVendedor)
class UsuarioVendedorAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "descripcion", "es_proveedor")
    search_fields = ("username", "email", "descripcion")
