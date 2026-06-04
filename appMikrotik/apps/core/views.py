from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm, FiltroLogs
from django.contrib.auth.decorators import login_required
from core.models import Logs


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def signout(request):
    logout(request)
    return redirect('login')

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            render(request, 'login.html', {'form':form}, {'error':'Formulario no valido'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logs(request):
    logs = Logs.objects.all()
    if request.method == 'POST':
        form = FiltroLogs(request.POST)
        if form.is_valid():
            fecha_inicio = form.cleaned_data.get('fecha_inicio')
            fecha_fin = form.cleaned_data.get('fecha_fin')

            if fecha_inicio and fecha_fin:
                logs = logs.filter(fecha__range=(fecha_inicio, fecha_fin))
            elif fecha_inicio:
                logs = logs.filter(fecha__gte=fecha_inicio)
            elif fecha_fin:
                logs = logs.filter(fecha__lte=fecha_fin)
    else:
        form = FiltroLogs()

    logs = logs.order_by('-fecha')
    return render(request, 'logs.html', {'logs': logs, 'filtros': form})
