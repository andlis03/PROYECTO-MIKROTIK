from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('gestion_pagos/<int:id>', login_required(views.gestion_pago), name='gestion_pagos'),
    path('crear_pago/', login_required(views.crear_pago), name='crear_pago'),
    path('modificar_pago/<int:id>/', login_required(views.modificar_pago), name='modificar_pago'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 