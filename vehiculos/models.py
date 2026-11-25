from django.db import models


class Vehiculo(models.Model):
    objects = models.Manager()

    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    anio = models.IntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=0)
    kilometraje = models.IntegerField()
    descripcion = models.TextField(blank=True)
    imagen_url = models.URLField(max_length=500, blank=True, default='')
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.marca} {self.modelo}"