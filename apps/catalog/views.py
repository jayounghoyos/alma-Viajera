from django import forms
from django.core.exceptions import ValidationError
from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from .models import Item

class CatalogView(View):
    template_name = 'catalog.html'

    def get(self, request, place, categoria, *args, **kwargs):
        search = request.GET.get("search")
        ordenar = request.GET.get("ordenar")  # <--- query param, e.g. ?ordenar=precio

        if search:
            items = Item.objects.filter(
                categoria__nombre=categoria, ubicacion=place, nombre=search
            )
        else:
            items = Item.objects.filter(
                categoria__nombre=categoria, ubicacion=place
            )

        # apply ordering
        if ordenar == "precio_asc":
            items = items.order_by("precio")
        elif ordenar == "precio_desc":
            items = items.order_by("-precio")
        elif ordenar == "tiempo_asc":  # placeholder if later you add ratings
            items = items.order_by("tiempo")  # example, replace with your field
        elif ordenar == "tiempo_desc":  # placeholder if later you add ratings
            items = items.order_by("-tiempo")  # example, replace with your field

        print(items)

        return render(request, "catalog.html", {
            "place": place,
            "categoria": categoria,
            "items": items,
        })
