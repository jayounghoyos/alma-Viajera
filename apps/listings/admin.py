from django.contrib import admin
from .models import Location, Place, LocalProduct, LocalService

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "state", "country")
    search_fields = ("city", "state", "country")

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "rating")
    list_filter = ("location__country", "location__city", "rating")
    search_fields = ("title", "location__city")

@admin.register(LocalProduct)
class LocalProductAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "where_to_buy")
    list_filter = ("location__country", "location__city")
    search_fields = ("name", "location__city", "where_to_buy")

@admin.register(LocalService)
class LocalServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "contact_name", "price_from")
    list_filter = ("location__country", "location__city")
    search_fields = ("title", "location__city", "contact_name")
