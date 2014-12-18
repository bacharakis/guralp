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

def detail(request, guralp):
    log_list = log.objects.filter(guralp_prefix=guralp)
    guralp_details = guralp.objects.filter(guralp_prefix=guralp)
    context = {'guralp_details' : guralp_details , 'log_list' : log_list }

    return render(request, 'guralp/guralp.html', context)
