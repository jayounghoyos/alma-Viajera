from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ProviderRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        return u.is_authenticated and getattr(u, 'es_proveedor', False)

    def handle_no_permission(self):
        return super().handle_no_permission()

class DashboardView(LoginRequiredMixin, ProviderRequiredMixin, TemplateView):
    template_name = 'providers/dashboard.html'

class OnboardingView(LoginRequiredMixin, ProviderRequiredMixin, TemplateView):
    template_name = 'providers/onboarding.html'
