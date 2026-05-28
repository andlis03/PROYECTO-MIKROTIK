from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required


# Create your views here.
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
