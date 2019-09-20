from django import template
from ..models import Direcciones
register = template.Library()

@register.inclusion_tag('customtags/selectDirectAll.html')
def selectDirectAll():
    direcciones = Direcciones.objects.filter(titular = None)
    return {'dirAll': direcciones}

@register.inclusion_tag('customtags/selectDirectFilter.html')
def selectDirectFilter():
    direcciones = Direcciones.objects.exclude(see_in_select = False)
    return {'dirFilter': direcciones}

@register.inclusion_tag('customtags/directActAll.html')
def showAllDirecActivities(user):
    activities = Direcciones.objects.exclude(see_in_list = False)
    return {'activities' : activities, 'user': user}

@register.inclusion_tag('customtags/directActFilter.html')
def showFilterDirectActivities(user):
    activities = user.direccion.actividades.all()
    direccion = user.direccion
    return {'activities' : activities, 'direct' : direccion, 'user': user}
