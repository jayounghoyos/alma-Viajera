# python
from abc import ABC, abstractmethod
from typing import Dict
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render


class QRExporter(ABC):
    """Interfaz base para exportadores."""
    @abstractmethod
    def export(self, request: HttpRequest, context: Dict) -> HttpResponse:
        raise NotImplementedError


class PDFExporter(QRExporter):
    """
    Exportador que usa Playwright para generar PDF.

    Requisitos:
      - pip install playwright
      - python -m playwright install chromium
    """
    def export(self, request: HttpRequest, context: Dict) -> HttpResponse:
        # import tardío para no romper el arranque si playwright no está instalado
        try:
            from playwright.sync_api import sync_playwright
        except Exception as exc:
            return HttpResponse(
                f"Playwright no está disponible: {exc}",
                status=500,
                content_type="text/plain",
            )

        # Renderizar la plantilla a HTML
        html_string = render_to_string("core/qr_pdf.html", context, request=request)

        # Si la plantilla usa rutas relativas, inyectar un <base> con la URL absoluta
        base_url = request.build_absolute_uri("/")
        if "<base " not in html_string:
            # Inserta el base justo después del <head> si existe
            if "<head>" in html_string:
                html_string = html_string.replace("<head>", f"<head><base href=\"{base_url}\">", 1)
            else:
                # si no hay head, prefiere no modificar
                pass

        pdf_bytes = None
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                page = browser.new_page()
                page.set_content(html_string, wait_until="networkidle")
                pdf_bytes = page.pdf(
                    format="A4",
                    print_background=True,
                    margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"},
                )
                browser.close()
        except Exception as exc:
            return HttpResponse(f"Error generando PDF: {exc}", status=500, content_type="text/plain")

        resp = HttpResponse(pdf_bytes, content_type="application/pdf")
        if request.GET.get("download") in ("1", "true", "yes"):
            resp["Content-Disposition"] = 'attachment; filename="reserva_qr.pdf"'
        else:
            resp["Content-Disposition"] = 'inline; filename="reserva_qr.pdf"'
        return resp


class HTMLExporter(QRExporter):
    """Devuelve HTML renderizado (por ejemplo para impresión)."""
    def export(self, request: HttpRequest, context: Dict) -> HttpResponse:
        html_string = render_to_string("core/qr_printable.html", context, request=request)
        return HttpResponse(html_string, content_type="text/html")


class QRViewExporter(QRExporter):
    """Exportador por defecto que renderiza la vista normal con `render`."""
    def export(self, request: HttpRequest, context: Dict) -> HttpResponse:
        return render(request, "core/qr_reservation.html", context)
