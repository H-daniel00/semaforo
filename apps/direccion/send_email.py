from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Correos_Notificacion

def send_notification_mail(from_user, to_user):
    if to_user is not None and from_user is not None:
        if Correos_Notificacion.objects.filter(usuario = to_user).exists():
            send_mail(
                'Notificación de Control Sedec',
                '',
                'controlsedec@tabasco.gob.mx',
                [to_user.correos.correo_inst, to_user.correos.correo_per],
                fail_silently=False,
                html_message= render_to_string('base/nueva_actividad_email.html', {'from_user': from_user.get_full_name, 'to_user': to_user.get_full_name}),
            )
        else:
            print('no tiene correos')
    else:
        print('el usuario no existe')