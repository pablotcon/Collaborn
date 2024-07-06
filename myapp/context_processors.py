from .models import Mensaje

def unread_messages_count(request):
    if request.user.is_authenticated:
        return {
            'unread_messages_count': Mensaje.objects.filter(receptor=request.user, leido=False).count()
        }
    return {
        'unread_messages_count': 0
    }
