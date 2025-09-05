from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class BaseSignupForm(forms.ModelForm):
    
    username   = forms.CharField(label="Usuario")                 
    first_name = forms.CharField(label="Nombre", required=False)  
    last_name  = forms.CharField(label="Apellido", required=False)
    email      = forms.EmailField(label="Email")

    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = User
        #Decidimos agregar más campos, mejorando las ociones de sign UP
        fields = ['username', 'first_name', 'last_name', 'email'] 

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Las contraseñas no coinciden.")
        if p1:
            validate_password(p1)
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class CustomerSignupForm(BaseSignupForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.es_proveedor = False
        if commit:
            user.save()
        return user

class ProviderSignupForm(BaseSignupForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.es_proveedor = True
        if commit:
            user.save()
        return user
    

class LoginForm(AuthenticationForm):
    """Permite iniciar sesión con username O email."""
    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username')
        password = cleaned.get('password')

        if username and password:
            # Intento normal (username)
            user = authenticate(self.request, username=username, password=password)
            if user is None and '@' in username:
                # Intento por email
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    u = User.objects.get(email__iexact=username)
                    user = authenticate(self.request, username=u.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is None:
                raise ValidationError(self.error_messages['invalid_login'], code='invalid_login')

            self.confirm_login_allowed(user)
            self.user_cache = user

        return cleaned