from django.forms import ModelForm
from core.models import Pago
from django import forms

class PagoForm(ModelForm):
    class Meta:
        model = Pago
        fields = ['montoUSD', 'tasa', 'metodo', 'comprobante', 'fecha']
        widgets = {
            'montoUSD': forms.NumberInput(attrs={'class': 'form-control'}),
            'tasa': forms.NumberInput(attrs={'class': 'form-control'}),
            'metodo': forms.Select(attrs={'class': 'form-select'}),
            'comprobante': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput( attrs={'class': 'form-control', 'type': 'date'}),
        }

class FiltroPagos(forms.Form):
    nombreCliente = forms.CharField(label='Nombre', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre o RIF', 'class': 'form-control'}))
    fecha_inicio = forms.DateField(label='Desde', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    fecha_fin = forms.DateField(label='Hasta', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

class FiltroPendientes(forms.Form):
    nombreCliente = forms.CharField(label='Nombre', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}))