from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from core.models import Pago, Logs, Cliente
from .forms import PagoForm, FiltroPagos
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def gestion_pago(request, id):
    pagos = Pago.objects.all().order_by('-fecha')

    if request.method == 'POST':
        filtro = FiltroPagos(request.POST)
        if filtro.is_valid():
            nombreCliente = filtro.cleaned_data.get('nombreCliente')
            fecha_inicio = filtro.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro.cleaned_data.get('fecha_fin')

            print(f"Nombre del cliente: {nombreCliente}, Fecha inicio: {fecha_inicio}, Fecha fin: {fecha_fin}") 

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
        if id != 0:
            pagos = pagos.filter(idCliente=id)
        
    return render(request, 'gestion_pagos.html', {'pagos': pagos, 'filtros': filtro})

@login_required
def crear_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST, request.FILES)

        if form.is_valid():
            idCliente = request.POST.get('idCliente')
            cliente = Cliente.objects.get(id=idCliente)

            if cliente.saldo == 0:
                return render(request, 'crear_pago.html', {
                    'form': form, 
                    'error': 'El cliente no tiene saldo pendiente.'
                    })

            montoUSD = form.cleaned_data.get('montoUSD')
            cliente.saldo -= montoUSD

            if cliente.saldo < 0:
                return render(request, 'crear_pago.html', {
                    'form': form, 
                    'error': 'El monto del pago excede el saldo pendiente del cliente.'
                    })
            elif cliente.saldo == 0:
                cliente.estado = 'Solvente'

            nuevoPago = form.save(commit=False)
            nuevoPago.idPersonal = request.user
            nuevoPago.save()

            cliente.save()

            Logs.objects.create(
                idPersonal=request.user,
                mensaje=f"""
                Registró un nuevo pago para el cliente {cliente.nombre} (Cédula: {cliente.cedula}). 
                Monto: {montoUSD}$
                Tasa: {nuevoPago.tasa}
                Comprobante: {nuevoPago.comprobante.url if nuevoPago.comprobante else 'Sin comprobante'}
                Fecha: {nuevoPago.fecha}
                """,
                modulo = "Gestion de pagos",
                error = False,
                fecha = timezone.now()
            )

            return redirect('gestion_pagos',0)
    else:
        form = PagoForm()
    return render(request, 'crear_pago.html', {'form': form})

@login_required
def modificar_pago(request, id):
    pago = get_object_or_404(Pago, id=id)

    clienteAnterior = pago.idCliente
    montoAnterior = pago.montoUSD

    if request.method == 'POST':
        form = PagoForm(request.POST, request.FILES, instance=pago)
        
        if form.is_valid():
            clienteNuevo = form.cleaned_data.get('idCliente')
            montoNuevo = form.cleaned_data.get('montoUSD')
            
            if clienteNuevo == clienteAnterior:
                diferencia = montoNuevo - montoAnterior
                clienteNuevo.saldo -= diferencia
                
                if clienteNuevo.saldo < 0:
                    return render(request, 'modificar_pago.html', {
                        'form': form, 
                        'error': 'El monto del pago excede el saldo pendiente del cliente.'
                    })
                elif clienteNuevo.saldo == 0:
                    clienteNuevo.estado = 'Solvente'
                else:
                    clienteNuevo.estado = 'Pendiente'

                clienteNuevo.save()
            else:
                clienteAnterior.saldo += montoAnterior
                clienteAnterior.estado = 'Pendiente'
                
                if clienteNuevo.saldo == 0:
                    return render(request, 'modificar_pago.html', {
                        'form': form, 
                        'error': 'El cliente seleccionado no tiene saldo pendiente.'
                    })
                    
                clienteNuevo.saldo -= montoNuevo
                
                if clienteNuevo.saldo < 0:
                    return render(request, 'modificar_pago.html', {
                        'form': form, 
                        'error': 'El monto del pago excede el saldo pendiente del cliente nuevo.'
                    })
                elif clienteNuevo.saldo == 0:
                    clienteNuevo.estado = 'Solvente'
                    
                clienteAnterior.save()
                clienteNuevo.save()

            nuevoPago = form.save(commit=False)
            nuevoPago.idPersonal = request.user
            nuevoPago.save()
            form.save_m2m()

            if clienteNuevo == clienteAnterior:
                Logs.objects.create(
                    idPersonal=request.user, 
                    mensaje=f"""
                    Modificó un pago del cliente {clienteNuevo.nombre} (Cédula: {clienteNuevo.cedula}). 
                    Monto anterior: {montoAnterior}$, Monto nuevo: {montoNuevo}$
                    Tasa anterior: {pago.tasa}, Tasa nueva: {form.cleaned_data.get('tasa')}
                    Comprobante anterior: {pago.comprobante.url if pago.comprobante else 'Sin comprobante'}, Comprobante nuevo: {nuevoPago.comprobante.url if nuevoPago.comprobante else 'Sin comprobante'}
                    Fecha anterior: {pago.fecha}, Fecha nueva: {form.cleaned_data.get('fecha')}
                    Personal anterior: {pago.idPersonal.username}, Personal nuevo: {request.user.username}
                    """,
                    modulo = "Gestion de pagos",
                    error = False,
                    fecha = timezone.now()
                )
            else:
                Logs.objects.create(
                    idPersonal=request.user, 
                    mensaje=f"""
                    Modificó un pago del cliente {clienteNuevo.nombre} (Cédula: {clienteNuevo.cedula}).
                    Para otro cliente {clienteAnterior.nombre} ((Cédula: {clienteAnterior.cedula}).
                    Monto anterior: {montoAnterior}$, Monto nuevo: {montoNuevo}$
                    Tasa anterior: {pago.tasa}, Tasa nueva: {form.cleaned_data.get('tasa')}
                    Comprobante anterior: {pago.comprobante.url if pago.comprobante else 'Sin comprobante'}, Comprobante nuevo: {nuevoPago.comprobante.url if nuevoPago.comprobante else 'Sin comprobante'}
                    Fecha anterior: {pago.fecha}, Fecha nueva: {form.cleaned_data.get('fecha')}
                    Personal anterior: {pago.idPersonal.username}, Personal nuevo: {request.user.username}""",
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
