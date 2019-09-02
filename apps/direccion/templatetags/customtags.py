from django import template
from ..models import Direcciones
register = template.Library()

@register.inclusion_tag('doctor/horarios.html')
def getDirectionsForReg(codeday, doctor):
    horarios = Horarios.objects.filter(dia__codenumber = codeday, doctor = doctor).order_by('hora')
    return {'horarios': horarios}
