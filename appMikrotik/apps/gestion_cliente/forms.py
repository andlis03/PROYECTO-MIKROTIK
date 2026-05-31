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
        
        return cedula_limpio


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
    
    def clean(self):
        cleaned_data = super().clean()
        
        campos_unicos = ['cedula', 'email', 'direccionIP', 'celular']
        
        for nombre_campo in campos_unicos:
            valor = cleaned_data.get(nombre_campo)
            
            if valor:
                filtros = {
                    nombre_campo: valor,
                    'borrado': False
                }
                consulta = Cliente.objects.filter(**filtros)
                
                if self.instance and self.instance.pk:
                    consulta = consulta.exclude(pk=self.instance.pk)
                
                if consulta.exists():
                    self.add_error(
                        nombre_campo, 
                        f"{nombre_campo} ya pertenece a un cliente activo en el sistema."
                    )
        
        return cleaned_data

