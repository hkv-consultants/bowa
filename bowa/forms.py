from django import forms


class ScenarioForm(forms.Form):
    name = forms.CharField(max_length=100, required=True,
                           help_text="Een naam voor dit scenario")
    email = forms.EmailField(required=True,
                             help_text="Uw email adres")
