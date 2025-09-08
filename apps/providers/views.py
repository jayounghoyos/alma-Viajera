from django.contrib import messages
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect

from .forms import ItemCreateForm


class ProviderRequiredMixin(UserPassesTestMixin):
    """Allow access only to authenticated users marked as providers."""
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and getattr(u, "es_proveedor", False)

    def handle_no_permission(self):
        messages.error(self.request, "Tu cuenta no es de proveedor.")
        return redirect("core:home")


class DashboardView(LoginRequiredMixin, ProviderRequiredMixin, TemplateView):
    """Simple dashboard for providers."""
    template_name = "providers/dashboard.html"


@method_decorator(login_required, name="dispatch")
class CrearServicioView(ProviderRequiredMixin, View):
    """
    Class-based view for creating an Item.
    - Requires user to be authenticated and provider (via mixins).
    - Never trusts the form for ownership; it always assigns the current user.
    """
    def get(self, request, *args, **kwargs):
        form = ItemCreateForm()
        return render(request, "providers/formulario.html", {"form": form})

    def post(self, request, *args, **kwargs):
        # Extra guard (mixin already checks, but this keeps it explicit)
        if not getattr(request.user, "es_proveedor", False):
            messages.error(request, "Tu cuenta no es de proveedor.")
            return redirect("core:home")

        form = ItemCreateForm(request.POST, request.FILES)
        if form.is_valid():
            # Do not commit yet; we need to set the owner (vendedor)
            item = form.save(commit=False)

            # IMPORTANT: The logged-in user is always the owner (vendedor)
            item.vendedor = request.user

            # Basic consistency: if not available and no stock provided, default to 0
            if item.disponibilidad is False and getattr(item, "stock", None) is None:
                item.stock = 0

            item.save()
            messages.success(request, "¡Servicio creado correctamente!")
            return redirect("providers:dashboard")

        # Invalid form: re-render with errors
        return render(request, "providers/formulario.html", {"form": form})


@login_required
def crear_servicio(request):
    """
    Function-based view for creating an Item.
    - Same logic as the CBV version.
    - Keeps ownership assignment server-side (never exposed in the form).
    """
    if not getattr(request.user, "es_proveedor", False):
        messages.error(request, "Tu cuenta no es de proveedor.")
        return redirect("core:home")

    if request.method == "POST":
        form = ItemCreateForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)

            # The logged-in user is always the owner (vendedor)
            item.vendedor = request.user

            # Basic consistency: if not available and no stock provided, default to 0
            if item.disponibilidad is False and getattr(item, "stock", None) is None:
                item.stock = 0

            item.save()
            messages.success(request, "¡Servicio creado correctamente!")
            return redirect("providers:dashboard")
    else:
        form = ItemCreateForm()

    return render(request, "providers/formulario.html", {"form": form})
