from django.db.models import Q
from .models import Place, LocalProduct, LocalService

def filter_catalog(params):
    """
    Aplica los mismos filtros a los tres catálogos.
    params: request.GET (q, country, city, min_price, max_price)
    Retorna dict con 3 querysets.
    """
    q = params.get("q") or ""
    country = params.get("country") or ""
    city = params.get("city") or ""
    minp = params.get("min_price") or ""
    maxp = params.get("max_price") or ""

    places = Place.objects.select_related("location")
    products = LocalProduct.objects.select_related("location")
    services = LocalService.objects.select_related("location")

    if q:
        places = places.filter(Q(title__icontains=q) | Q(description__icontains=q))
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
        services = services.filter(Q(title__icontains=q) | Q(description__icontains=q))

    if country:
        places = places.filter(location__country__icontains=country)
        products = products.filter(location__country__icontains=country)
        services = services.filter(location__country__icontains=country)

    if city:
        places = places.filter(location__city__icontains=city)
        products = products.filter(location__city__icontains=city)
        services = services.filter(location__city__icontains=city)

    if minp:
        services = services.filter(price_from__gte=minp)
    if maxp:
        services = services.filter(price_from__lte=maxp)

    return {"places": places, "products": products, "services": services}
