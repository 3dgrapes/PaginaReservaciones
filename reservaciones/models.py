from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20)
    departamento = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Sala(models.Model):
    nombre = models.CharField(max_length=20)
    capacidad_max = models.IntegerField(default=40)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    canal = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField()

    class Meta:
        verbose_name_plural = "Solicitudes"

    def __str__(self):
        return f"Solicitud de {self.usuario.nombre} - {self.estado}"

class Evento(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    nombre_evento = models.CharField(max_length=200)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    asistentes_esperados = models.IntegerField()
    asistentes_reales = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=20)
    descripcion = models.TextField()
    requerimientos = models.TextField(blank=True)
    salas = models.ManyToManyField(Sala)

    def __str__(self):
        return self.nombre_evento

