import base64
import json
from django.shortcuts import render, get_object_or_404, redirect
from apps.catalog.models import Item
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Carrito, CarritoItem
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.utils.translation import gettext as _


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
    request.session['qr_payload'] = _build_cart_qr_payload(carrito)
    return render(request, 'cart.html', {'carrito': carrito, 'login_required': False})


def _build_cart_qr_payload(carrito):
    items = carrito.items.select_related('item').all()
    if not items:
        return "cart-empty"
    data = {
        "user": carrito.usuario_id,
        "generated_at": now().isoformat(),
        "total": str(carrito.total),
        "items": [
            {
                "id": cart_item.item_id,
                "name": cart_item.item.nombre,
                "qty": cart_item.cantidad,
            }
            for cart_item in items
        ],
    }
    raw = json.dumps(data, separators=(',', ':'), ensure_ascii=True)
    return base64.urlsafe_b64encode(raw.encode()).decode()


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
        return HttpResponseBadRequest(_("No se encontró un cliente válido."))

    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, item=item)
    if not created:
        carrito_item.cantidad += 1
        carrito_item.save()

    carrito.calcular_total()
    request.session['qr_payload'] = _build_cart_qr_payload(carrito)
    return redirect('cart:detalle')


# Mantengo csrf_exempt para evitar problemas si tu setup actual lo requiere,
# pero revisa si puedes quitarlo y usar CSRF normal (tu JS ya envía X-CSRFToken).
@csrf_exempt
def incrementar_cantidad(request, item_id):
    if request.method != 'POST':
        return JsonResponse({'error': _('Método no permitido')}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'error': _('Debes iniciar sesión'), 'login_url': reverse('users:login')}, status=403)

    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito:
        return JsonResponse({'error': _('Carrito no encontrado')}, status=404)

    carrito_item = CarritoItem.objects.filter(carrito=carrito, item__id=item_id).first()
    if not carrito_item:
        return JsonResponse({'error': _('Producto no encontrado en el carrito')}, status=404)

    carrito_item.cantidad += 1
    carrito_item.save()
    carrito.calcular_total()
    request.session['qr_payload'] = _build_cart_qr_payload(carrito)

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
        return JsonResponse({'error': _('Método no permitido')}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'error': _('Debes iniciar sesión'), 'login_url': reverse('users:login')}, status=403)

    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito:
        return JsonResponse({'error': _('Carrito no encontrado')}, status=404)

    carrito_item = CarritoItem.objects.filter(carrito=carrito, item__id=item_id).first()
    if not carrito_item:
        return JsonResponse({'error': _('Producto no encontrado en el carrito')}, status=404)

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
    request.session['qr_payload'] = _build_cart_qr_payload(carrito)
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
        return JsonResponse({'error': _('Debes iniciar sesión'), 'login_url': reverse('users:login')}, status=403)

    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito:
        return JsonResponse({'error': _('Carrito no encontrado')}, status=404)

    carrito_item = CarritoItem.objects.filter(carrito=carrito, item__id=item_id).first()
    if not carrito_item:
        return JsonResponse({'error': _('Producto no encontrado en el carrito')}, status=404)

    carrito_item.delete()
    carrito.calcular_total()
    total = float(carrito.total)
    request.session['qr_payload'] = _build_cart_qr_payload(carrito)

    return JsonResponse({'total': total})
