from django.urls import path
from .views import LoginView, LogoutView, SignupCustomerView, SignupProviderView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupCustomerView.as_view(), name='signup_customer'),
    path('providers/signup/', SignupProviderView.as_view(), name='signup_provider'),
]