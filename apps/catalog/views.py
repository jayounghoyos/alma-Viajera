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

    def get(self, request):
        category = request.GET.get("category")  # e.g. "comida"
        if category:
            items = Item.objects.filter(categoria__nombre=category)
        else:
            items = Item.objects.filter(categoria__nombre="lugar")
        viewData = {
            "items": items,
            "selected_category": category
        }
        return render(request, self.template_name, viewData)