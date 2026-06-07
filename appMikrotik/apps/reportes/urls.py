from django.urls import path
from .views import gestion_reportes, api_datos_reportes

urlpatterns = [
    path('gestion_reportes/', gestion_reportes, name='gestion_reportes'),

    path('api/datos-reportes/', api_datos_reportes, name='api_datos_reportes'),
]