#python
# File: `apps/core/views.py`
from django.shortcuts import render
from django.http import HttpRequest
import base64
import json
from urllib.parse import quote_plus
from .services.exporters import PDFExporter, HTMLExporter, QRExporter

def _safe_b64_decode(s: str) -> str:
    if not s:
        raise ValueError("empty")
    b = s.encode() if isinstance(s, str) else s
    padding = (-len(b)) % 4
    b += b'=' * padding
    return base64.urlsafe_b64decode(b).decode()

def build_qr_context(request: HttpRequest) -> dict:
    qr_payload = request.GET.get('code') or request.session.get('qr_payload') or 'cart-empty'
    qr_url = (
        "https://api.qrserver.com/v1/create-qr-code/"
        f"?size=300x300&data={quote_plus(qr_payload)}"
    )
    cart_summary = None
    try:
        decoded = _safe_b64_decode(qr_payload)
        cart_summary = json.loads(decoded)
    except Exception:
        cart_summary = None
    return {
        "qr_url": qr_url,
        "qr_payload": qr_payload,
        "cart_summary": cart_summary,
    }

def qr_reservation(request: HttpRequest):
    context = build_qr_context(request)
    return render(request, 'core/qr_reservation.html', context)

def export_qr(request: HttpRequest, reservation_id: int = None, exporter: QRExporter = None):
    context = build_qr_context(request)
    exporter = exporter or PDFExporter()
    return exporter.export(request, context)
