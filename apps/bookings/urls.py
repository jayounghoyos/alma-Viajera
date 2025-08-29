from django.urls import path
from .views import BookingsPlaceholderView

app_name = "bookings"

urlpatterns = [
    path("", BookingsPlaceholderView.as_view(), name="list"),
]
