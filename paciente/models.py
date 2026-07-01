from django.db import models
from medicina.models import Medicina

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()

    medicinas = models.ManyToManyField(Medicina, blank=True)

    def __str__(self):
        return self.nombre