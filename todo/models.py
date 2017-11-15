from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Nota(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField(blank=True)
    usuario = models.ForeignKey(User)
    publico = models.BooleanField(default=True)

    def __str__(self):
        return self.title