from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = 'user/login.html'

class LogoutView(TemplateView):
    template_name = 'user/login.html'  # placeholder; luego será una acción

class SignupCustomerView(TemplateView):
    template_name = 'user/signup_customer.html'

class SignupProviderView(TemplateView):
    template_name = 'user/signup_provider.html'
