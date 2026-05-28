from django.forms import ModelForm, forms
from core.models import Cliente
import re 

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['idPlan', 'nombre', 'cedula', 'celular', 'direccion', 'email', 'direccionIP']


    def clean_cedula(self):
            
            cedula = self.cleaned_data.get('cedula')
            
            cedula_limpia = re.sub(r'[-.\s]', '', str(cedula))
            
            if not cedula_limpia.isdigit():
                raise forms.ValidationError("La cédula debe contener solo números.")
                
            if not (6 <= len(cedula_limpia) <= 9):
                raise forms.ValidationError("La cédula debe tener una longitud válida (entre 6 y 9 dígitos).")
                
            return cedula_limpia


    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        
        celular_limpio = re.sub(r'[-.\s()+=]', '', str(celular))
        
        if not celular_limpio.isdigit():
            raise forms.ValidationError("El número de celular debe contener solo números.")
            
        if len(celular_limpio) != 11:
            raise forms.ValidationError("El número celular debe tener exactamente 11 dígitos (Ej: 04141234567).")
            
        return celular_limpio


    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if direccion:
            
            direccion = direccion.strip().upper()  
            
            if len(direccion) < 15:
                raise forms.ValidationError("Por favor, introduce una dirección más detallada para el equipo técnico (mínimo 15 caracteres).")
                
        return direccion