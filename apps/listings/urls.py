from django.urls import path
from .views import ExplorerView

app_name = "listings"
urlpatterns = [
    path("explorar/", ExplorerView.as_view(), name="explorer"),
]
