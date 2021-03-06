from .models import Page
from datetime import datetime

def help(request):
    return {'help_pages':Page.objects.filter(type='help')}

def current_time(request):
    return { 'time_now' : datetime.now() }

def server_load(request):
    try:
        with open('/proc/loadavg','rt') as file:
            server_load = float( file.readline().split()[0] )
    except Exception as e:
        server_load = '?'
    return { 'server_load' : server_load }
