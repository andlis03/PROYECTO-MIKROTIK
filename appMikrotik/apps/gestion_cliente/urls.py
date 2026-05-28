from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('gestion_cliente/<int:id>', login_required(views.gestion_cliente), name='gestion_clientes'),
    path('crear_cliente/', login_required(views.crear_cliente), name='crear_cliente'),
    path('modificar_cliente/<int:id>/', login_required(views.modificar_cliente), name='modificar_cliente'),
    path('borrar_cliente/<int:id>/', login_required(views.borrar_cliente), name='confirmar_borrado')
]