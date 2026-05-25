from django.contrib import admin
from .models import Cliente, Plan, Factura, Pago, Logs

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Plan)
admin.site.register(Factura)
admin.site.register(Pago)
admin.site.register(Logs)
