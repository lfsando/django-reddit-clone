from django.utils import timezone


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = timezone.now()
    diff = timezone.now()  # default
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "agora mesmo"
        if second_diff < 60:
            return str(round(second_diff)) + " segundos atrás"
        if second_diff < 120:
            return "a minuto ago"
        if second_diff < 3600:
            return str(round(second_diff / 60)) + " minutos atrás"
        if second_diff < 7200:
            return "uma hora atrás"
        if second_diff < 86400:
            return str(round(second_diff / 3600)) + " horas atrás"
    if day_diff == 1:
        return "Ontem"
    if day_diff < 7:
        return str(round(day_diff, 1)) + " dias atrás"
    if day_diff < 31:
        return str(round(day_diff / 7, 1)) + " semanas atrás"
    if day_diff < 365:
        return str(round(day_diff / 30)) + " meses atrás"
    return str(round(day_diff / 365, 2)) + " anos atrás"
