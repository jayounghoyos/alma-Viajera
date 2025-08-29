from django.views.generic import TemplateView
from django.db.models import Q
from .models import Place, LocalProduct, LocalService

class ExplorerView(TemplateView):
    template_name = "listings/explorer.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = self.request.GET.get("q") or ""
        country = self.request.GET.get("country") or ""
        city = self.request.GET.get("city") or ""
        minp = self.request.GET.get("min_price") or ""
        maxp = self.request.GET.get("max_price") or ""

        places = Place.objects.select_related("location")
        products = LocalProduct.objects.select_related("location")
        services = LocalService.objects.select_related("location")

        if q:
            places   = places.filter(Q(title__icontains=q) | Q(description__icontains=q))
            products = products.filter(Q(name__icontains=q)  | Q(description__icontains=q))
            services = services.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if country:
            places   = places.filter(location__country__icontains=country)
            products = products.filter(location__country__icontains=country)
            services = services.filter(location__country__icontains=country)
        if city:
            places   = places.filter(location__city__icontains=city)
            products = products.filter(location__city__icontains=city)
            services = services.filter(location__city__icontains=city)
        if minp:
            services = services.filter(price_from__gte=minp)
        if maxp:
            services = services.filter(price_from__lte=maxp)

        ctx.update({"places": places, "products": products, "services": services})
        return ctx
