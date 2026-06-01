from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('gestion_pagos/<int:id>', views.gestion_pago, name='gestion_pagos'),
    path('crear_pago/', views.crear_pago, name='crear_pago'),
    path('modificar_pago/<int:id>/', views.modificar_pago, name='modificar_pago'),
    path('detalles_pago/<int:id>/', views.mostrar_detalles, name='detalles_pago'),
    path('pendientes/', views.pagos_pendientes, name='pagos_pendientes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 