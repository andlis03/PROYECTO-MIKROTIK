from django.forms import ModelForm
from core.models import Cliente 

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'cedula', 'celular', 'direccion', 'email', 'estado']