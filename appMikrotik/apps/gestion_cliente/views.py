from django.shortcuts import render, redirect, get_object_or_404
from core.models import Cliente
from .forms import ClienteForm

def crear_cliente(request):
if request.method == 'POST':
    form = ClienteForm(request.POST)
    if form.is_valid():
        form.save() 
        return redirect('lista_clientes') 
else:
    form = ClienteForm() 

return render(request, 'clientes/crear_cliente.html', {'form': form})



def modificar_cliente(request, id):
cliente = get_object_or_404(Cliente, id=id)

if request.method == 'POST':
    form = ClienteForm(request.POST, instance=cliente)
    if form.is_valid():
        form.save() 
        return redirect('lista_clientes')
else:
    form = ClienteForm(instance=cliente)

return render(request, 'clientes/modificar_cliente.html', {'form': form, 'cliente': cliente})


def borrar_cliente(request, id):
cliente = get_object_or_404(Cliente, id=id)

if request.method == 'POST':

    cliente.borrado = True
    cliente.save()
    
    return redirect('lista_clientes')
    
return render(request, 'clientes/confirmar_borrado.html', {'cliente': cliente})