from django.http import HttpResponse
from django.shortcuts import render
from guralp.models import guralp, log, status
import pycurl
from io import BytesIO

# Create your views here.
def index(request):

    latest_guralp_list = guralp.objects.order_by('prefix')
    log_list = log.objects.all()

    context = {'latest_guralp_list': latest_guralp_list ,'log_list' : log_list }

    return render(request, 'guralp/index.html', context)

def detail(request, guralpre):
    log_list = log.objects.filter(guralp_prefix=guralpre)
    status_list = status.objects.filter(guralp_prefix=guralpre)
    guralp_details = guralp.objects.filter(prefix=guralpre)
    context = {'guralp_details' : guralp_details , 'log_list' : log_list , 'status_list' : status_list }

    return render(request, 'guralp/guralp.html', context)
