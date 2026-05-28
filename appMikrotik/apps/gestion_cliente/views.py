from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from core.models import Cliente, Logs, Factura
from .forms import ClienteForm

def gestion_cliente(request,id):
    if id == 0:
        objetos = Cliente.objects.filter(borrado = False)
    else:
        objetos = Cliente.objects.filter(idCliente=id, borrado = False)

    return render(request, 'gestion_clientes.html', {'clientes': objetos}) 

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            
            cliente = form.save(commit=False)
            
            cliente.estado = 'Pendiente'         
            cliente.saldo = cliente.idPlan.precioUSD 
            cliente.borrado = False       
            
            cliente.save()  

            Factura.objects.create(
                idCliente=cliente,            
                montoUSD=cliente.idPlan.precioUSD,
                fecha=timezone.now()  
            )

            Logs.objects.create(
                idPersonal=request.user,
                mensaje=f"""
                Registró al nuevo cliente {cliente.nombre} (Cédula: {cliente.cedula}).
                Celular: {cliente.celular}
                Email: {cliente.email}
                Direccion: {cliente.direccion}
                Plan: {cliente.idPlan.plan} 
                Direccion Ip:{cliente.direccionIP}
                Estado: {cliente.estado}
                """,
                modulo="Gestión de Clientes",
                error=False,
                fecha=timezone.now()
            )

            return redirect('gestion_clientes', 0) 
    else:
        form = ClienteForm() 

    return render(request, 'crear_cliente.html', {'form': form})


def modificar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    planAnterior = cliente.idPlan
    estadoAnterior = cliente.estado
    saldoAnterior = cliente.saldo

    if request.method == 'POST':
        cliente_viejo = Cliente.objects.get(id=id)
        
        form = ClienteForm(request.POST, instance=cliente)
        
        if form.is_valid():
            cliente = form.save(commit=False)

            if cliente.idPlan != planAnterior:

                if cliente.estado in ['Exonerado', 'Solvente']:
                    cliente.saldo = 0.00
                else:
                    cliente.saldo = cliente.idPlan.precio
                    cliente.estado = 'Pendiente' 
                    
                    Factura.objects.create(
                        idCliente=cliente,            
                        montoUSD=cliente.idPlan.precio,
                        fecha=timezone.now()  
                    )

            else:
                if cliente.estado in ['Exonerado', 'Solvente']:
                    cliente.saldo = 0.00
                    
                elif cliente.estado == 'Desconectado':
                    if saldoAnterior == 0.00:
                        cliente.saldo = cliente.idPlan.precio
                    else:
                        cliente.saldo = saldoAnterior
                        
                else: # cliente.estado == 'Pendiente
                    cliente.saldo = saldoAnterior

            cliente.save()

            lista_cambios = []

            for campo, valor_nuevo in cliente.__dict__.items():

                if campo.startswith('_') or campo in ['id', 'borrado']:
                    continue
                
                valor_viejo = getattr(cliente_viejo, campo)
                
                if valor_nuevo != valor_viejo:
                    lista_cambios.append(f"{campo}: {valor_viejo} => {valor_nuevo}")

            if lista_cambios:
                mensaje_log = f"Modificó al cliente {cliente.nombre} (ID: {cliente.id}). Cambios realizados:\n" + "\n".join(lista_cambios)
            else:
                mensaje_log = f"El operador guardó al cliente {cliente.nombre} (ID: {cliente.id}) sin realizar cambios."

            Logs.objects.create(
                idPersonal=request.user,
                mensaje=mensaje_log,
                modulo="Gestión de Clientes",
                error=False,
                fecha=timezone.now()
            )

            return redirect('gestion_clientes', 0)
            
    else:
        form = ClienteForm(instance=cliente)
        
    return render(request, 'modificar_cliente.html', {'form': form, 'cliente': cliente})


def borrar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        ip_eliminada = cliente.direccionIP
        
        cliente.borrado = True
        cliente.saldo = 0.00         
        cliente.estado = 'Desactivado'   
        cliente.direccionIP = None

        cliente.save()

        Logs.objects.create(
                idPersonal=request.user,
                mensaje=f"""
                Se Elimino al cliente {cliente.nombre} (Cédula: {cliente.cedula}).
                Celular: {cliente.celular}
                Email: {cliente.email}
                Direccion: {cliente.direccion}
                Plan: {cliente.idPlan.plan} 
                Direccion Ip:{ip_eliminada}
                Estado: {cliente.estado}
                """,
                modulo="Gestión de Clientes",
                error=False,
                fecha=timezone.now()
            )
        
        return redirect('gestion_clientes', 0)
        
    return render(request, 'confirmar_borrar.html', {'cliente': cliente})