from django.shortcuts import render
from .models import Carrito

def carrito_view(request):
    carrito = None
    if request.user.is_authenticated:
        # Usuario autenticado: buscar el carrito asociado
        carrito = Carrito.objects.filter(usuario_id=request.user).first()
        if not carrito:
            carrito = {'items': [], 'total': 0}  # Carrito vacío para usuarios autenticados sin carrito
    else:
        # Usuario no autenticado: inicializar un carrito vacío
        carrito = {'items': [], 'total': 0}

    return render(request, 'carrito.html', {'carrito': carrito})