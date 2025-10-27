# Juan Andrés Young Hoyos
from django.shortcuts import render
from django.views.generic import TemplateView
import base64
import json
from urllib.parse import quote_plus
# Create your views here.


class HomeView(TemplateView):
    """ View para el home y que probablemente va a heredarle a los otros"""
    template_name = 'core/home.html'


def qr_reservation(request):
    qr_payload = request.GET.get('code') or request.session.get('qr_payload') or 'cart-empty'
    qr_url = (
        "https://api.qrserver.com/v1/create-qr-code/"
        f"?size=300x300&data={quote_plus(qr_payload)}"
    )
    cart_summary = None
    try:
        decoded = base64.urlsafe_b64decode(qr_payload.encode()).decode()
        cart_summary = json.loads(decoded)
    except Exception:
        cart_summary = None
    context = {
        "qr_url": qr_url,
        "qr_payload": qr_payload,
        "cart_summary": cart_summary,
    }
    return render(request, 'core/qr_reservation.html', context)
