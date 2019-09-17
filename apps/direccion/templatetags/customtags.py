from django import template
from ..models import Direcciones
register = template.Library()

@register.inclusion_tag('customtags/selectDirectAll.html')
def selectDirectAll():
    direcciones = Direcciones.objects.filter(titular = None)
    return {'dirAll': direcciones}

@register.inclusion_tag('customtags/selectDirectFilter.html')
def selectDirectFilter():
    direcciones = Direcciones.objects.exclude(codename = 'sg')
    return {'dirFilter': direcciones}

@register.inclusion_tag('customtags/directActAll.html')
def showAllDirecActivities():
    activities = Direcciones.objects.exclude(codename = 'sg')
    return {'activities' : activities}

@register.inclusion_tag('customtags/directActFilter.html')
def showFilterDirectActivities(user):
    activities = user.direccion.actividades.all()
    direccion = user.direccion
    return {'activities' : activities, 'direct' : direccion}
