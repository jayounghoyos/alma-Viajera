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
    ordenar_por_precio = True
    ordenar_estrella = True
    def get(self, request, place, categoria, *args, **kwargs):
        items = Item.objects.filter(categoria__nombre=categoria, ubicacion=place)
        
        return render(request, "catalog.html", {
            "place": place,
            "categoria": categoria,
            "items": items,
        })