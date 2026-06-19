"""
URL configuration for PaginaReservaciones project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reservaciones.views import eventos_json, salas_json, evento_detalle, eventos_del_dia, agenda, actualizar_evento

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calendario/', eventos_json, name="calendario"),
    path('salas/', salas_json, name="sala"),
    path('agenda/', agenda, name="agenda"),
    path('actualizar-evento/<int:evento_id>/', actualizar_evento, name="actualizar_evento"),
    path('evento/<int:evento_id>/', evento_detalle, name="evento_detalle"),
    path('evento_dia/<str:fecha>/', eventos_del_dia, name="filtrar_evento_dia"),
]
