from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home'),
    path('signout/', login_required(views.signout), name='signout'),
    path('login/', views.signin, name='login'),
]