from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from earthquakes.models import stations, events
from django.core import serializers
import pytz
import datetime


def stations_api(request):

    if request.method == 'GET':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.

        #Always use get on request.POST. Correct way of querying a QueryDict.
        name = request.GET.get('name')
        code = request.GET.get('code')
        fi = request.GET.get('fi')
        lamda = request.GET.get('lamda')
        height = request.GET.get('height')

        data = serializers.serialize('json', stations.objects.filter(station_name__icontains=name)\
        .filter(station_code__icontains=code)\
        .filter(fi__icontains=fi)\
        .filter(lamda__icontains=lamda)\
        .filter(height__icontains=height) )


        return JsonResponse(data, safe=False)

    return render(request, 'earthquakes/index.html')

def events_api(request):

    if request.method == 'GET':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.

        #Always use get on request.POST. Correct way of querying a QueryDict.
        eventID = request.GET.get('eventID')
        eventStartDate = request.GET.get('eventStartDate')
        eventEndDate = request.GET.get('eventEndDate')
        eventHighMMF = request.GET.get('eventHighMMF')
        eventLowMMF = request.GET.get('eventLowMMF')
        eventHighDepth = request.GET.get('eventHighDepth')
        eventLowDepth = request.GET.get('eventLowDepth')


        dt=datetime.datetime.strptime(eventStartDate, "%a %b %d %Y").date()
        dtt=datetime.datetime.strptime(eventEndDate, "%a %b %d %Y").date()
        filteredEvents = events.objects.all()

        if eventID:
            filteredEvents = filteredEvents.filter(event_id=eventID)

        if eventStartDate and eventEndDate:
            filteredEvents = filteredEvents.filter(datetime__range=[dt, dtt])

        if eventLowDepth and eventHighDepth:
            filteredEvents = filteredEvents.filter(depth__gte=eventLowDepth, depth__lte=eventHighDepth)

        if eventLowMMF and eventHighMMF:
            filteredEvents = filteredEvents.filter(mmf__gte=eventLowMMF, mmf__lte=eventHighMMF)

        data = serializers.serialize('json', filteredEvents)

        return JsonResponse(data, safe=False)

    return render(request, 'earthquakes/index.html')



def search(req):
    if req.GET:
        search_term = req.GET['term']
        results = stations.objects.filter(id=search_term)
        results="SKG"
        return render( {'results': results},'index.html')
    return render('index.html', {})

def index(request):

    stations_list = stations.objects.all().order_by('station_code')


    return render(request, 'earthquakes/index.html', { 'stations_list' : stations_list } )
