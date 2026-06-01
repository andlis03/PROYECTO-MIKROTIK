from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from core.models import Pago, Logs, Cliente
from .forms import PagoForm, FiltroPagos, FiltroPendientes
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def gestion_pago(request):
    pagos = Pago.objects.all().order_by('-fecha')

    if request.method == 'POST':
        filtro = FiltroPagos(request.POST)
        if filtro.is_valid():
            nombreCliente = filtro.cleaned_data.get('nombreCliente')
            fecha_inicio = filtro.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro.cleaned_data.get('fecha_fin')

            if nombreCliente:
                pagos = pagos.filter(idCliente__nombre__icontains=nombreCliente)

            if fecha_inicio and fecha_fin:
                pagos = pagos.filter(fecha__range=(fecha_inicio, fecha_fin))
            elif fecha_inicio:
                pagos = pagos.filter(fecha__gte=fecha_inicio)
            elif fecha_fin:
                pagos = pagos.filter(fecha__lte=fecha_fin)

            pagos = pagos.order_by('-fecha')
    else:
        filtro = FiltroPagos()
        
    return render(request, 'gestion_pagos.html', {'pagos': pagos, 'filtros': filtro})

@login_required
def crear_pago(request,id):
    cliente = get_object_or_404(Cliente,borrado=False, id=id)

    if request.method == 'POST':
        form = PagoForm(request.POST, request.FILES)

        if form.is_valid():
            montoUSD = form.cleaned_data.get('montoUSD')
            cliente.saldo -= montoUSD

            if cliente.saldo < 0:
                return render(request, 'crear_pago.html', {
                    'form': form, 
                    'error': 'El monto del pago excede el saldo pendiente del cliente.'
                    })
            elif cliente.saldo == 0:
                cliente.estado = 'Solvente'

            nuevo_pago = form.save(commit=False)
            nuevo_pago.idPersonal = request.user
            nuevo_pago.save()

            cliente.save()

            Logs.objects.create(
                idPersonal=request.user,
                mensaje=f"""Registró un nuevo pago para el cliente {cliente.nombre} (Cédula: {cliente.cedula}). 
Monto: {montoUSD}$
Tasa: {nuevo_pago.tasa}""",
                modulo = "Gestion de pagos",
                error = False,
                fecha = timezone.now()
            )

            return redirect('gestion_pagos',0)
    else:
        form = PagoForm()
    return render(request, 'crear_pago.html', {'form': form, 'cliente': cliente})

@login_required
def modificar_pago(request, id):
    pago = get_object_or_404(Pago, id=id)
    montoAnterior = pago.montoUSD

    if request.method == 'POST':
        form = PagoForm(request.POST, request.FILES, instance=pago)
        
        if form.is_valid():
            cliente = form.cleaned_data.get('idCliente')
            montoNuevo = form.cleaned_data.get('montoUSD')            
            diferencia = montoNuevo - montoAnterior
            cliente.saldo -= diferencia
                
            if cliente.saldo < 0:
                return render(request, 'modificar_pago.html', {
                    'form': form, 
                    'error': 'El monto del pago excede el saldo pendiente del cliente.'
                })
            elif cliente.saldo == 0:
                cliente.estado = 'Solvente'
            else:
                cliente.estado = 'Pendiente'

            cliente.save()

            pago = form.save(commit=False)
            pago.idPersonal = request.user
            pago.save()
            form.save_m2m()

            lista_cambios = []

            for campo, valor_nuevo in pago.__dict__.items():

                if campo.startswith('_') or campo in ['id', 'borrado']:
                    continue
                
                valor_viejo = getattr(pago, campo)
                
                if valor_nuevo != valor_viejo:
                    lista_cambios.append(f"{campo}: {valor_viejo} => {valor_nuevo}")

            if lista_cambios:
                mensaje_log = f"Modificó al pago (ID: {pago.id}). Cambios realizados:\n\n" + "\n".join(lista_cambios)
            else:
                mensaje_log = f"El operador guardó al pago (ID: {pago.id}) sin realizar cambios."
            
            Logs.objects.create(
                idPersonal=request.user, 
                mensaje=mensaje_log,
                modulo = "Gestion de pagos",
                error = False,
                fecha = timezone.now()
            )
            
            return redirect('gestion_pagos', 0)
    else:
        form = PagoForm(instance=pago)
        
    return render(request, 'modificar_pago.html', {'form': form})

@login_required
def mostrar_detalles(request, id):
    pago = get_object_or_404(Pago, id=id)
    cliente = pago.idCliente
    return render(request, 'detalles_pago.html', {'pago': pago, 'cliente': cliente})

@login_required
def pendientes(request):
    clientes = Cliente.objects.filter(borrado=False,saldo__gt=0).order_by('nombre')

    if request.method == 'POST':
        filtro = FiltroPendientes(request.POST)
        if filtro.is_valid():
            nombreCliente = filtro.cleaned_data.get('nombreCliente')

            if nombreCliente:
                clientes = clientes.filter(nombre__icontains=nombreCliente)

    return render(request, 'pendientes.html', {'clientes': clientes, 'filtros': filtro})
