from django import template
from django.utils import timezone
from ..models import Direcciones, Actividades
register = template.Library()

@register.inclusion_tag('customtags/selectDirectAll.html')
def selectDirectAll():
    direcciones = Direcciones.objects.filter(titular = None, is_active = True)
    return {'dirAll': direcciones}

@register.inclusion_tag('customtags/selectDirectFilter.html')
def selectDirectFilter():
    direcciones = Direcciones.objects.exclude(see_in_select = False, is_active = False)
    return {'dirFilter': direcciones}

@register.inclusion_tag('customtags/directActAll.html')
def showAllDirecActivities(user, year, assigned = False):
    if assigned:
        activities = user.direccion.subdir.filter(see_in_list = True, is_active = True)
    else:
        activities = Direcciones.objects.exclude(see_in_list = False, is_active = False)
    return {'activities': activities, 'user': user, 'current_year': year}

@register.inclusion_tag('customtags/directActFilter.html')
def showFilterDirectActivities(user, year):
    activities = user.direccion.actividades.filter(direccion__see_in_list = True, direccion__is_active = True)
    direccion = user.direccion
    return {'activities': activities, 'direct': direccion, 'user': user, 'current_year': year}

@register.inclusion_tag('customtags/activity.html')
def getNewActivitiesByYear(direct, user, year):
    activities = direct.actividades.filter(timestamp__year = year)
    return {'activities': activities, 'user': user}

@register.inclusion_tag('customtags/activity_old.html')
def getOldActivitiesByYear(direct, user, year):
    activities = direct.actividades.filter(timestamp__year__lt = year)
    return {'activities': activities, 'user': user, 'total_old': len(activities)}

@register.inclusion_tag('customtags/priority_select.html')
def prioritySelect(opt_selected, act_id):
    return {'choices': Actividades.prioridad_choices, 'opt_selected': opt_selected, 'act_id': act_id}
