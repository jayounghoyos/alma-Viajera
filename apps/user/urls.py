# Juan Andrés Young Hoyos
from django.urls import path
from django.urls import path
from .views import SimpleLoginView, SimpleLogoutView, SignupCustomerView, SignupProviderView  # de views.py



app_name = 'users'

urlpatterns = [
    path('login/', SimpleLoginView.as_view(), name='login'),
    path('logout/', SimpleLogoutView.as_view(), name='logout'),
    path('signup/', SignupCustomerView.as_view(), name='signup_customer'),
    path('providers/signup/', SignupProviderView.as_view(), name='signup_provider'),
]
