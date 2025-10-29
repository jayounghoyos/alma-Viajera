# Juan Andrés Young Hoyos
from django.contrib import messages
from django.views.generic import TemplateView, View, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.translation import gettext as _

from .forms import ItemCreateForm
from apps.catalog.models import Item, Categoria


class ProviderRequiredMixin(UserPassesTestMixin):
    """Allow access only to authenticated users marked as providers."""
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and getattr(u, "es_proveedor", False)

    def handle_no_permission(self):
        messages.error(self.request, _("Tu cuenta no es de proveedor."))
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
            messages.error(request, _("Tu cuenta no es de proveedor."))
            return redirect("core:home")

        form = ItemCreateForm(request.POST, request.FILES)
        if form.is_valid():
            # Do not commit yet; we need to set the owner (vendedor)
            item = form.save(commit=False)

            # IMPORTANT: The logged-in user is always the owner (vendedor)
            item.vendedor = request.user

            # Handle categoria - get or create the category object from POST data
            categoria_nombre = request.POST.get('categoria')
            categoria_obj, created = Categoria.objects.get_or_create(nombre=categoria_nombre)
            item.categoria = categoria_obj

            # Basic consistency: if not available and no stock provided, default to 0
            if item.disponibilidad is False and getattr(item, "stock", None) is None:
                item.stock = 0

            item.save()
            messages.success(request, _("¡Servicio creado correctamente!"))
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
        messages.error(request, _("Tu cuenta no es de proveedor."))
        return redirect("core:home")

    if request.method == "POST":
        form = ItemCreateForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)

            # The logged-in user is always the owner (vendedor)
            item.vendedor = request.user

            # Handle categoria - get or create the category object from POST data
            categoria_nombre = request.POST.get('categoria')
            categoria_obj, created = Categoria.objects.get_or_create(nombre=categoria_nombre)
            item.categoria = categoria_obj

            # Basic consistency: if not available and no stock provided, default to 0
            if item.disponibilidad is False and getattr(item, "stock", None) is None:
                item.stock = 0

            item.save()
            messages.success(request, _("¡Servicio creado correctamente!"))
            return redirect("providers:dashboard")
    else:
        form = ItemCreateForm()

    return render(request, "providers/formulario.html", {"form": form})


class VerServiciosView(LoginRequiredMixin, ProviderRequiredMixin, ListView):
    """Vista para mostrar todos los servicios del vendedor autenticado."""
    model = Item
    template_name = "providers/ver_servicios.html"
    context_object_name = "servicios"
    paginate_by = 10

    def get_queryset(self):
        """Filtrar solo los servicios del vendedor autenticado."""
        return Item.objects.filter(vendedor=self.request.user).order_by('-id')


class EditarServicioView(LoginRequiredMixin, ProviderRequiredMixin, UpdateView):
    """Vista para editar un servicio existente."""
    model = Item
    form_class = ItemCreateForm
    template_name = "providers/editar_servicio.html"
    success_url = reverse_lazy('providers:ver_servicios')

    def get_queryset(self):
        """Solo permitir editar servicios del vendedor autenticado."""
        return Item.objects.filter(vendedor=self.request.user)

    def get_object(self):
        """Obtener el objeto y verificar que pertenece al usuario."""
        obj = get_object_or_404(Item, pk=self.kwargs['pk'], vendedor=self.request.user)
        return obj

    def form_valid(self, form):
        """Mensaje de éxito al editar."""
        messages.success(self.request, _("¡Servicio actualizado correctamente!"))
        return super().form_valid(form)

    def form_invalid(self, form):
        """Mensaje de error si el formulario es inválido."""
        messages.error(self.request, _("Por favor, corrige los errores en el formulario."))
        return super().form_invalid(form)


class EliminarServicioView(LoginRequiredMixin, ProviderRequiredMixin, DeleteView):
    """Vista para eliminar un servicio."""
    model = Item
    success_url = reverse_lazy('providers:ver_servicios')

    def get_queryset(self):
        """Solo permitir eliminar servicios del vendedor autenticado."""
        return Item.objects.filter(vendedor=self.request.user)

    def get_object(self):
        """Obtener el objeto y verificar que pertenece al usuario."""
        obj = get_object_or_404(Item, pk=self.kwargs['pk'], vendedor=self.request.user)
        return obj

    def delete(self, request, *args, **kwargs):
        """Mensaje de éxito al eliminar."""
        messages.success(request, _("¡Servicio eliminado correctamente!"))
        return super().delete(request, *args, **kwargs)


@login_required
def eliminar_servicio_ajax(request, pk):
    """Vista AJAX para eliminar un servicio."""
    if not getattr(request.user, "es_proveedor", False):
        return JsonResponse({'error': _('No tienes permisos para realizar esta acción.')}, status=403)

    try:
        servicio = get_object_or_404(Item, pk=pk, vendedor=request.user)
        servicio.delete()
        return JsonResponse({'success': True, 'message': _('Servicio eliminado correctamente.')})
    except Exception as e:
        return JsonResponse({'error': _('Error al eliminar el servicio.')}, status=500)
