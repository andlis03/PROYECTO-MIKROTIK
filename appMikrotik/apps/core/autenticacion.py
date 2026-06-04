from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

# Este archivo define la función decoradora grupo_requerido, 
# que se utiliza para restringir el acceso a ciertas vistas a usuarios que pertenecen a un grupo específico.
# La función verifica si el usuario es un superusuario o si pertenece al grupo requerido, 
# y lanza una excepción de permiso denegado si no cumple con los requisitos.
def grupo_requerido(grupo_nombre):
    def check_grupo(user):
        if user.is_superuser:
            return True
        if user.groups.filter(name=grupo_nombre).exists():
            return True
        raise PermissionDenied
    return user_passes_test(check_grupo)