from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Plan(models.Model):
    plan = models.CharField(max_length=20)
    precioUSD = models.DecimalField(max_digits=10, decimal_places=2)
    velocidad_subida = models.DecimalField(max_digits=10, decimal_places=2)
    velocidad_bajada = models.DecimalField(max_digits=10, decimal_places=2)
    borrado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.plan} {self.precioUSD} {self.velocidad_subida} {self.velocidad_bajada}"
    
class Cliente(models.Model):
    idPlan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    cedula = models.CharField(max_length=9, unique=True)
    celular = models.CharField(max_length=12)
    direccion = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    direccionIP = models.GenericIPAddressField(protocol='IPv4', unique=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=20, default='Activo')
    borrado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cedula} {self.nombre}  {self.celular} {self.direccion} {self.email} {self.direccionIP} {self.saldo} {self.direccion} {self.estado}"
    
class Factura(models.Model):
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    montoUSD = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.idCliente} {self.montoUSD} {self.fecha}"

class Pago(models.Model):
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    idPersonal = models.ForeignKey(User, on_delete=models.CASCADE)
    montoUSD = models.DecimalField(max_digits=10, decimal_places=2)
    tasa = models.DecimalField(max_digits=10, decimal_places=2)
    pagoUSD = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    comprobante = models.FileField(upload_to='comprobantes/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return f"{self.idCliente} {self.idPersonal} {self.montoUSD} {self.tasa} {self.pagoUSD} {self.fecha}"
    
class Logs(models.Model):
    idPersonal = models.ForeignKey(User, on_delete=models.CASCADE)
    modulo = models.CharField(max_length=30)
    mensaje = models.TextField()
    error = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.idPersonal} {self.modulo} {self.mensaje} {self.error} {self.fecha}"