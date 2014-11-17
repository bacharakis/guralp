from django.http import HttpResponse
from django.shortcuts import render
from guralp.models import guralp, log
import pycurl
from io import BytesIO

# Create your views here.
def index(request):

    latest_guralp_list = guralp.objects.all()
    log_list = log.objects.all()

    context = {'latest_guralp_list': latest_guralp_list ,'log_list' : log_list }

    return render(request, 'guralp/index.html', context)

def detail(request, guralp_prefix):
    log_list = log.objects.filter(guralps_prefix="SEIS")
    latest_guralp_list = guralp.objects.all()
    context = {'latest_guralp_list' : latest_guralp_list , 'log_list' : log_list }

    return render(request, 'guralp/guralp.html', context)
