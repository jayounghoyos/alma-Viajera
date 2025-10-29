from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Item
from .forms import CalificacionForm
from django.http import JsonResponse, Http404

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
    template_name = 'catalog/item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()

        context['calificacion_form'] = CalificacionForm()
        context['promedio_calificacion'] = item.promedio_calificacion()
        context['calificaciones'] = item.calificaciones.all()
        context['rango_estrellas'] = range(1, 6)

        # Agregamos estrellas en el contexto

        context['estrellas'] = item.estrellas()

        return context

    def post(self, request, *args, **kwargs):
        item = self.get_object()
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.item = item
            calificacion.usuario = request.user
            try:
                calificacion.save()
                messages.success(request, _("¡Gracias por tu calificación!"))
            except:
                messages.error(request, _("Ya has calificado este producto."))
        else:
            messages.error(request, _("Hubo un error al enviar tu calificación."))
        return redirect('catalog:item_detail', pk=item.pk)

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

def item_detail_api(request, id):
    try:
        item = Item.objects.select_related('categoria', 'vendedor').get(id=id)
    except Item.DoesNotExist:
        raise Http404(_("Item not found"))

    data = {
        "id": item.id,
        "nombre": item.nombre,
        "descripcion": item.descripcion,
        "precio": str(item.precio),
        "categoria": item.categoria.nombre,
        "ubicacion": item.ubicacion,
        "imagen": item.imagen.url if item.imagen else None,
        "tiempo": float(item.tiempo) if item.tiempo else None,
        "disponibilidad": item.disponibilidad,
        "stock": item.stock,
        "promedio_calificacion": item.promedio_calificacion(),
        "estrellas": item.estrellas(),
        "vendedor": item.vendedor.username,
    }

    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
