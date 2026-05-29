from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):

    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        self.fields['username'].widget.attrs.update({
        'class': 'form-control custom-input',
        'placeholder': 'Nombre de usuario'
        })

        self.fields['password'].widget.attrs.update({
        'class': 'form-control custom-input',
        'placeholder': 'Contraseña'
        })

class FiltroLogs(forms.Form):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)