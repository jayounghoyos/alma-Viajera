# Juan Andrés Young Hoyos
from django import forms
from apps.catalog.models import Item

class ItemCreateForm(forms.ModelForm):
    disponibilidad = forms.ChoiceField(
        choices=[("1", "Disponible"), ("0", "No disponible")],
        widget=forms.Select,
    )

    class Meta:
        model = Item
        fields = [
            "nombre", "descripcion", "precio",
            "ubicacion", "imagen", "tiempo", "disponibilidad", "stock",
        ]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 4}),
        }


    def clean_disponibilidad(self):
        val = self.cleaned_data["disponibilidad"]
        return True if val in ("1", 1, True, "true", "True") else False