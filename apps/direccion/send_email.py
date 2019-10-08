from django.core.mail import send_mail
from .models import Correos_Notificacion

def send_notification_mail(from_user, to_user):
    if to_user is not None and from_user is not None:
        if Correos_Notificacion.objects.filter(usuario = to_user).exists():
            print(to_user.correos)
            send_mail(
                'Notificación de Control Sedec',
                'Se le ha asignado una nueva actividad por ' + from_user.get_full_name(),
                'davidernesto@tabasco.gob.mx',
                [to_user.correos.correo_inst, to_user.correos.correo_per],
                fail_silently=False,
            )
        else:
            print('no tiene correos')
    else:
        print('el usuario no existe')