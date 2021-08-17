# response.set_cookie('last_connection', datetime.datetime.now())
from django.http import HttpResponse
import datetime


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body><h1>It is now %s.</h1></body></html>" % now
    print(dir(request))
    return HttpResponse(html)
