from django.forms import ModelForm
from core.models import Pago

class PagoForm(ModelForm):
    class Meta:
        model = Pago
        fields = ['idCliente','montoUSD', 'tasa', 'metodo', 'comprobante', 'fecha']