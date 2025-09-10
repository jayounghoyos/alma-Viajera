from django.shortcuts import render, get_object_or_404, redirect
from apps.catalog.models import Item
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Carrito, CarritoItem
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def carrito_view(request):
    # Si no está logueado mostramos el mensaje de login_required en la plantilla
    if not request.user.is_authenticated:
        login_url = reverse('users:login')
        return render(request, 'cart.html', {
            'carrito': None,
            'login_required': True,
            'login_url': login_url
        })

    # Usuario autenticado: obtener o crear carrito
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'cart.html', {'carrito': carrito, 'login_required': False})


def requiere_inicio_sesion(request):
    next_url = reverse('cart:detalle')  # URL del carrito
    login_url = f"{reverse('users:login')}?next={next_url}"
    return render(request, 'cart.html', {'login_required': True, 'login_url': login_url})

@login_required
def agregar_al_carrito(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    try:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("No se encontró un cliente válido.")

    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, item=item)
    if not created:
        carrito_item.cantidad += 1
        carrito_item.save()

    carrito.calcular_total()
    return redirect('cart:detalle')


# Mantengo csrf_exempt para evitar problemas si tu setup actual lo requiere,
# pero revisa si puedes quitarlo y usar CSRF normal (tu JS ya envía X-CSRFToken).
@csrf_exempt
def incrementar_cantidad(request, item_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Debes iniciar sesión', 'login_url': reverse('users:login')}, status=403)

    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito:
        return JsonResponse({'error': 'Carrito no encontrado'}, status=404)

    carrito_item = CarritoItem.objects.filter(carrito=carrito, item__id=item_id).first()
    if not carrito_item:
        return JsonResponse({'error': 'Producto no encontrado en el carrito'}, status=404)

    carrito_item.cantidad += 1
    carrito_item.save()
    carrito.calcular_total()

    subtotal_item = float(carrito_item.cantidad * carrito_item.item.precio)
    total = float(carrito.total)

    return JsonResponse({
        'cantidad': carrito_item.cantidad,
        'subtotal_item': subtotal_item,
        'total': total
    })


@csrf_exempt
def decrementar_cantidad(request, item_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Debes iniciar sesión', 'login_url': reverse('users:login')}, status=403)

    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito:
        return JsonResponse({'error': 'Carrito no encontrado'}, status=404)

    carrito_item = CarritoItem.objects.filter(carrito=carrito, item__id=item_id).first()
    if not carrito_item:
        return JsonResponse({'error': 'Producto no encontrado en el carrito'}, status=404)

    if carrito_item.cantidad > 1:
        carrito_item.cantidad -= 1
        carrito_item.save()
        carrito.calcular_total()
        subtotal_item = float(carrito_item.cantidad * carrito_item.item.precio)
    else:
        # Si se llega a 0, borramos el CarritoItem
        carrito_item.delete()
        carrito.calcular_total()
        subtotal_item = 0.0

    total = float(carrito.total)
    cantidad = carrito_item.cantidad if carrito_item.id else 0

    return JsonResponse({
        'cantidad': cantidad,
        'subtotal_item': subtotal_item,
        'total': total
    })


@csrf_exempt
@require_POST
def eliminar_del_carrito(request, item_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Debes iniciar sesión', 'login_url': reverse('users:login')}, status=403)

    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito:
        return JsonResponse({'error': 'Carrito no encontrado'}, status=404)

    carrito_item = CarritoItem.objects.filter(carrito=carrito, item__id=item_id).first()
    if not carrito_item:
        return JsonResponse({'error': 'Producto no encontrado en el carrito'}, status=404)

    carrito_item.delete()
    carrito.calcular_total()
    total = float(carrito.total)

    return JsonResponse({'total': total})
