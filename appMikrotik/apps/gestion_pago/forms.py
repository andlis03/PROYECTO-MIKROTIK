from django.forms import ModelForm
from core.models import Pago
from django import forms

# Este archivo define los formularios utilizados en la gestión de pagos, incluyendo el formulario para registrar y modificar pagos,
# así como los formularios de filtro para la lista de pagos y la lista de clientes con pagos pendientes.

class PagoForm(ModelForm):
    class Meta:
        model = Pago
        fields = ['montoUSD', 'tasa', 'metodo', 'comprobante', 'fecha']
        widgets = {
            'montoUSD': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'metodo': forms.Select(attrs={'class': 'form-select'}),
            'comprobante': forms.FileInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class FiltroPagos(forms.Form):
    nombreCliente = forms.CharField(label='Nombre', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre o Cedula', 'class': 'form-control'}))
    fecha_inicio = forms.DateField(label='Desde', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    fecha_fin = forms.DateField(label='Hasta', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

class FiltroPendientes(forms.Form):
    nombreCliente = forms.CharField(label='Nombre o Cedula', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre o Rif', 'class': 'form-control'}))