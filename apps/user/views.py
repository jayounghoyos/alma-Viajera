from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView
from django.contrib.auth import login

from .forms import LoginForm, CustomerSignupForm, ProviderSignupForm


class SimpleLoginView(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_template_names(self):
        # Siempre renderizamos el parcial cuando es petición de modal
        return ['user/partials/login_modal.html']

    def get(self, request, *args, **kwargs):
        # Si NO viene como modal, redirige a Home y autoabre modal
        if request.headers.get('HX-Request') or request.GET.get('partial'):
            return super().get(request, *args, **kwargs)
        home = reverse('core:home')
        return redirect(f"{home}?open=login")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Si vino por modal, cerramos con HX-Redirect
        if self.request.headers.get('HX-Request') or self.request.GET.get('partial'):
            r = HttpResponse(status=204)
            r['HX-Redirect'] = self.get_success_url()
            return r
        return response

    def get_success_url(self):
        u = self.request.user
        if getattr(u, 'es_proveedor', False):
            return reverse_lazy('providers:dashboard')
        return reverse_lazy('core:home')


class SimpleLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')


class SignupCustomerView(FormView):
    form_class = CustomerSignupForm
    success_url = reverse_lazy('core:home')

    def get_template_names(self):
        return ['user/partials/signup_customer_modal.html']

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') or request.GET.get('partial'):
            return super().get(request, *args, **kwargs)
        home = reverse('core:home')
        return redirect(f"{home}?open=signup_customer")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        if self.request.headers.get('HX-Request') or self.request.GET.get('partial'):
            r = HttpResponse(status=204)
            r['HX-Redirect'] = str(self.success_url)
            return r
        return super().form_valid(form)


class SignupProviderView(FormView):
    form_class = ProviderSignupForm
    success_url = reverse_lazy('providers:dashboard')

    def get_template_names(self):
        return ['user/partials/signup_provider_modal.html']

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request') or request.GET.get('partial'):
            return super().get(request, *args, **kwargs)
        home = reverse('core:home')
        return redirect(f"{home}?open=signup_provider")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        if self.request.headers.get('HX-Request') or self.request.GET.get('partial'):
            r = HttpResponse(status=204)
            r['HX-Redirect'] = str(self.success_url)
            return r
        return super().form_valid(form)
