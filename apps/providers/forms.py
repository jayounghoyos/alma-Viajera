from django import forms
from apps.catalog.models import Item, Categoria

class ItemCreateForm(forms.ModelForm):
    disponibilidad = forms.ChoiceField(
        choices=[("1", "Disponible"), ("0", "No disponible")],
        widget=forms.Select,
    )

    class Meta:
        model = Item
        fields = [
            "categoria", "nombre", "descripcion", "precio",
            "ubicacion", "imagen", "tiempo", "disponibilidad", "stock",
        ]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].queryset = Categoria.objects.all().order_by("nombre")
        self.fields["categoria"].empty_label = "Selecciona una categoría"

    def clean_disponibilidad(self):
        val = self.cleaned_data["disponibilidad"]
        return True if val in ("1", 1, True, "true", "True") else False
