from django.urls import path
from .views import DashboardView, OnboardingView

urlpatterns = [
    path('account/', DashboardView.as_view(), name='dashboard'),
    path('onboarding/', OnboardingView.as_view(), name='onboarding'),
]
