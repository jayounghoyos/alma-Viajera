# Juan Andrés Young Hoyos
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login
from .forms import CustomerSignupForm, ProviderSignupForm

class SignupCustomerView(FormView):
    template_name = 'user/signup_customer.html'
    form_class = CustomerSignupForm
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)          # autologin
        return super().form_valid(form)

class SignupProviderView(FormView):
    template_name = 'user/signup_provider.html'
    form_class = ProviderSignupForm
    success_url = reverse_lazy('providers:dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)          # autologin
        return super().form_valid(form)
