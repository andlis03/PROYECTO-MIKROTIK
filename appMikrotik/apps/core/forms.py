from django.contrib.auth.forms import AuthenticationForm

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