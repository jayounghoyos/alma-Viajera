from django import forms
from .models import Calificacion

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['puntuacion', 'comentario']
        widgets = {
            'puntuacion': forms.RadioSelect(choices=[(i, f"{i} estrellas") for i in range(1, 6)]),
        }