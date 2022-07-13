# response.set_cookie('last_connection', datetime.datetime.now())
from django.http import HttpResponse

from django.shortcuts import render
import datetime


def current_datetime(request):
    now = datetime.datetime.now()
    html = f"<html><body><h1>It is now {now}.</h1></body></html>"
    print(dir(request))
    return HttpResponse(html)


def index(request):
    return render(request, "clients/index.html")
