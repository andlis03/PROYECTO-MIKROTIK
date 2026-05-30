from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.signin, name='login'),
    path('signout/', views.signout, name='signout'),
    path('logs/', login_required(views.logs), name='logs'),
]