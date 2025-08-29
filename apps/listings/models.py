from django.db import models

# Create your models here.

class Location(models.Model):
    country = models.CharField(max_length=80)
    state = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=80)

    class Meta:
        unique_together = ("country", "state", "city")
        ordering = ["country", "state", "city"]

    def __str__(self):
        return ", ".join([p for p in [self.city, self.state, self.country] if p])

class Place(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="places")
    contact_name = models.CharField(max_length=120, blank=True)
    contact_phone = models.CharField(max_length=40, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self): return self.title

class LocalProduct(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="local_products")
    where_to_buy = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self): return self.name

class LocalService(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="local_services")
    contact_name = models.CharField(max_length=120)
    contact_phone = models.CharField(max_length=40)
    price_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self): return self.title
