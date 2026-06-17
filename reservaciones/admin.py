from django.contrib import admin
from .models import Usuario, Sala, Solicitud, Evento

admin.site.register(Usuario)
admin.site.register(Sala)
admin.site.register(Solicitud)
admin.site.register(Evento)