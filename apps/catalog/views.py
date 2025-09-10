from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from .models import Item

class CatalogView(View):
    template_name = 'catalog.html'

    def get(self, request, place, categoria, *args, **kwargs):
        search = request.GET.get("search")
        ordenar = request.GET.get("ordenar")

        # Lista de países válidos
        paises_validos = ['Colombia', 'Mexico', 'Argentina', 'Peru', 'Chile', 'Brasil']
        
        # Si el lugar no está en la lista de países válidos, redirigir a Colombia por defecto
        if place not in paises_validos:
            place = 'Colombia'

        filters = {
            "categoria__nombre": categoria,
            "ubicacion": place,
            "disponibilidad": True,
        }

        if search:
            filters["nombre__icontains"] = search

        items = Item.objects.filter(**filters)

        # apply ordering
        if ordenar == "precio_asc":
            items = items.order_by("precio")
        elif ordenar == "precio_desc":
            items = items.order_by("-precio")
        elif ordenar == "tiempo_asc":
            items = items.order_by("tiempo")
        elif ordenar == "tiempo_desc":
            items = items.order_by("-tiempo")

        return render(request, "catalog.html", {
            "place": place,
            "categoria": categoria,
            "items": items,
        })


class ItemDetailView(DetailView):
    model = Item
    template_name = 'catalog/item_detail.html'  # Ruta directa sin la carpeta adicional
    context_object_name = 'item'


class MapView(TemplateView):
    """Vista para mostrar el mapa de selección de países."""
    template_name = 'catalog/map.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Lista de países disponibles (puedes expandir esto)
        context['paises'] = [
            {'codigo': 'Colombia', 'nombre': 'Colombia', 'lat': 4.5709, 'lng': -74.2973},
            {'codigo': 'Mexico', 'nombre': 'México', 'lat': 23.6345, 'lng': -102.5528},
            {'codigo': 'Argentina', 'nombre': 'Argentina', 'lat': -38.4161, 'lng': -63.6167},
            {'codigo': 'Peru', 'nombre': 'Perú', 'lat': -9.1900, 'lng': -75.0152},
            {'codigo': 'Chile', 'nombre': 'Chile', 'lat': -35.6751, 'lng': -71.5430},
            {'codigo': 'Brasil', 'nombre': 'Brasil', 'lat': -14.2350, 'lng': -51.9253},
        ]
        return context