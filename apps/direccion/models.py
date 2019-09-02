from django.db import models
from django.contrib.auth.models import AbstractUser

class Direcciones(models.Model):
    nombre = models.CharField(max_length = 100)
    codename = models.CharField(max_length = 5)
    titular = models.OneToOneField('direccion.Usuarios', on_delete = models.CASCADE, null = True, blank = True)
    def __str__(self):
        return '{}'.format(self.nombre)

class Usuarios(AbstractUser):
    direccion = models.ForeignKey(Direcciones, null = True, blank = True, on_delete = models.PROTECT)
    avatar = models.ImageField(upload_to = 'avatar/', null = True, blank = True)

    def is_secretary(self):
        if self.direccion.codename == 'sg':
            return True
        else:
            return False

class Actividades(models.Model):
    nombre = models.CharField(max_length = 200)
    timestamp = models.DateTimeField(auto_now = True)
    direccion = models.ForeignKey(Direcciones, null = True, blank = True, related_name = 'actividades' , on_delete = models.CASCADE)
    usuario = models.ForeignKey(Usuarios, blank = True, on_delete = models.CASCADE)

    def get_porcent(self):
        total = self.objetivos.count()
        total_done = self.objetivos.filter(is_done = True).count()
        return getPercentActivity(total_done, total)
    
    def get_light(self):
        total = self.objetivos.count()
        total_done = self.objetivos.filter(is_done = True).count()
        return getLightActivity(total_done, total)

class Objetivos(models.Model):
    nombre = models.CharField(max_length = 200)
    is_done = models.BooleanField(default = False)
    actividad = models.ForeignKey(Actividades, null = True, blank = True, related_name = 'objetivos' , on_delete = models.CASCADE)

def getPercentActivity(num, total):
    try:
        percent = (100 * num)/total
        return round(percent)
    except:
        return 0

def getLightActivity(num, total):
    red_color = '#f44336'
    green_color = '#4caf50'
    yellow_color = '#ffeb3b'
    green_light = 100
    yellow_light = 70
    try:
        percent = getPercentActivity(num, total)
        if percent == green_light:
            return green_color
        elif percent < green_light and percent >= yellow_light:
            return yellow_color
        elif percent < yellow_light:
            return red_color
    except:
        return red_color



