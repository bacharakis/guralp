from django.http import HttpResponse
from django.shortcuts import render
from guralp.models import guralp, log, status,logging
import pycurl
from io import BytesIO

# Create your views here.
def index(request):

    latest_guralp_list = guralp.objects.order_by('station_code')
    log_list = log.objects.all()
    logging_list = logging.objects.all()

    context = {'latest_guralp_list': latest_guralp_list ,'log_list' : log_list , 'logging_list' : logging_list }

    return render(request, 'guralp/index.html', context)

def detail(request, guralpre):
    log_list = log.objects.filter(station_code=guralpre)
    status_list = status.objects.filter(station_code=guralpre)
    guralp_details = guralp.objects.filter(station_code=guralpre)
    context = {'guralp_details' : guralp_details , 'log_list' : log_list , 'status_list' : status_list }

    return render(request, 'guralp/guralp.html', context)
