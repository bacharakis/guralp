from django.http import HttpResponse
from django.shortcuts import render
from guralp.models import guralp, single_log, history,logging
import pycurl
from io import BytesIO

# Create your views here.
def index(request):

    latest_guralp_list = guralp.objects.exclude(status="Unreachable").order_by('station_code')
    single_log_list = single_log.objects.all()
    history_list = history.objects.all()

    context = {'latest_guralp_list': latest_guralp_list ,'single_log_list' : single_log_list , 'history_list' : history_list }

    return render(request, 'guralp/index.html', context)

def detail(request, guralpre):
    single_log_list = single_log.objects.filter(station_code=guralpre)
    history_list = history.objects.filter(station_code=guralpre)
    guralp_details = guralp.objects.filter(station_code=guralpre)
    context = {'guralp_details' : guralp_details , 'single_log_list' : single_log_list , 'history_list' : history_list }

    return render(request, 'guralp/guralp.html', context)
