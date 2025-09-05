from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class SimpleLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True  # si ya está logueado, no muestra login

    def get_success_url(self):
        user = self.request.user
        # Redirección por rol:
        if getattr(user, 'es_proveedor', False):
            return reverse_lazy('providers:dashboard')
        return reverse_lazy('core:home')

class SimpleLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')
