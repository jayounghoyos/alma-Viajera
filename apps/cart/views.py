from django.shortcuts import render, get_object_or_404
from .models import Carrito

def carrito_view(request):
    if request.user.is_authenticated:
        # Usuario autenticado: buscar el carrito asociado
        carrito = Carrito.objects.filter(usuario_id=request.user).first()
        if not carrito:
            return render(request, 'carrito.html', {'error': 'No tienes un carrito asociado.'})
        return render(request, 'carrito.html', {'carrito': carrito})
    else:
        # Usuario no autenticado: manejar el caso
        return render(request, 'carrito.html', {'error': 'Debes iniciar sesión para acceder al carrito.'})