from django.forms import ModelForm, forms, BooleanField
from core.models import Cliente
from django.forms.widgets import CheckboxInput
import re 

class ClienteForm(ModelForm):
    
    exonerar_cliente = BooleanField(
        required=False,
        widget= CheckboxInput(attrs={'class': 'form-check-input'}),
        initial=False
    )

    class Meta:
        model = Cliente
        fields = ['idPlan', 'nombre', 'cedula', 'celular', 'direccion', 'email', 'direccionIP']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['exonerar_cliente'].initial = (self.instance.estado == 'Exonerado')    


    def clean_cedula(self):
            
        cedula = self.cleaned_data.get('cedula')
        
        cedula_limpio = re.sub(r'[-.\s]', '', str(cedula))
        
        if not cedula_limpio.isdigit():
            raise forms.ValidationError("La cédula debe contener solo números.")
            
        if not (6 <= len(cedula_limpio) <= 9):
            raise forms.ValidationError("La cédula debe tener una longitud válida (entre 6 y 9 dígitos), ejemplo 30759412.")
        
        if 'cedula' not in self.changed_data:
            return cedula

        if Cliente.objects.filter(cedula=cedula_limpio, borrado=False).exists():
            raise forms.ValidationError("Esta cédula ya pertenece a un cliente activo.")
            
        return cedula_limpio


    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        
        celular_limpio = re.sub(r'[-.\s()+=]', '', str(celular))

        if not celular_limpio.isdigit():
            raise forms.ValidationError("El número de celular debe contener solo números.")
            
        if len(celular_limpio) != 11:
            raise forms.ValidationError("El número celular debe tener exactamente 11 dígitos (Ej: 04141234567).")
        
        if 'celular' not in self.changed_data:
            return celular_limpio

        if Cliente.objects.filter(celular=celular_limpio, borrado=False).exists():
            raise forms.ValidationError("Este celular ya pertenece a un cliente activo.")
            
        return celular_limpio


    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')

        if direccion:
            
            direccion = direccion.strip().upper()  
            
            if len(direccion) < 15:
                raise forms.ValidationError("Por favor, introduce una dirección más detallada para el equipo técnico (mínimo 15 caracteres).")
                
        if 'direccion' not in self.changed_data:
            return direccion

        if Cliente.objects.filter(direccion=direccion, borrado=False).exists():
            raise forms.ValidationError("Esta direccion ya pertenece a un cliente activo.")

        return direccion
    
    
    def clean_direccionIP(self):
        direccionIP = self.cleaned_data.get('direccionIP')

        if 'direccionIP' not in self.changed_data:
            return direccionIP

        if Cliente.objects.filter(direccionIP=direccionIP, borrado=False).exists():
            raise forms.ValidationError("Esta direccionIP ya pertenece a un cliente activo.")
        
        return direccionIP
