#from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class HomeView(TemplateView):
    """ View para el home y que probablemente va a heredarle a los otros"""
    template_name = 'core/home.html'
