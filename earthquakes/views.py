from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from earthquakes.models import stations, events
from django.core import serializers
import pytz
from array import *
import datetime,math,cmath


def stations_api(request):

    if request.method == 'GET':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.

        #Always use get on request.POST. Correct way of querying a QueryDict.
        name = request.GET.get('name')
        code = request.GET.get('code')
        fi = request.GET.get('fi')
        lamda = request.GET.get('lamda')
        height = request.GET.get('height')
        A = request.GET.get('A')
        F = request.GET.get('F')
        zoom = request.GET.get('zoom')
        soilClass = request.GET.get('soilClass')
        vs30High = request.GET.get('vs30High')
        vs30Low = request.GET.get('vs30Low')
        owner = request.GET.get('owner')

        filteredStations=stations.objects.filter(station_name__icontains=name)\
        .filter(station_code__startswith=code.upper())\
        .filter(height__icontains=height) \
        .filter(soil_class__icontains=soilClass) \
        .filter(owner__icontains=owner)

        if vs30High and vs30Low:
            filteredStations=filteredStations.filter(vs30__gte=vs30Low, vs30__lte=vs30High)

        #Distance (in km from the center of the map to the edges
        zoomlevel = array("i",[1000000, 100000, 10000 , 1000 , 600, 500 , 400 ,300 , 170, 100, 80, 60, 50, 40, 30, 10, 5, 4, 3, 2, 1, 1])

        tmp = []
        for station in filteredStations.all():
            #Degrees to radians
            lat1=(float(A) * math.pi /180)
            long1=(float(F) * math.pi/180)
            lat2=(float(station.fi) * math.pi /180)
            long2=(float(station.lamda) * math.pi /180)

            #Calculate the distance between two points
            if(math.acos(math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(long1-long2)) * 6371 <= float(zoomlevel[int(zoom)])):
                tmp.append(station.id)

        #Get only the events in the area
        filteredStations=filteredStations.filter(id__in=tmp)

        data = serializers.serialize('json', filteredStations)

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
        A = request.GET.get('A')
        F = request.GET.get('F')
        zoom = request.GET.get('zoom')

        dt=datetime.datetime.strptime(eventStartDate, "%a %b %d %Y").date()
        dtt=datetime.datetime.strptime(eventEndDate, "%a %b %d %Y").date()
        filteredEvents = events.objects.all()

        if eventID:
            filteredEvents = filteredEvents.filter(event_id__icontains=eventID)

        if eventStartDate and eventEndDate:
            filteredEvents = filteredEvents.filter(datetime__range=[dt, dtt])

        if eventLowDepth and eventHighDepth:
            filteredEvents = filteredEvents.filter(depth__gte=eventLowDepth, depth__lte=eventHighDepth)

        if eventLowMMF and eventHighMMF:
            filteredEvents = filteredEvents.filter(mmf__gte=eventLowMMF, mmf__lte=eventHighMMF)

        #Distance (in km from the center of the map to the edges
        zoomlevel = array("i",[1000000, 100000, 10000 , 1000 , 600, 500 , 400 ,300 , 170, 100, 80, 60, 50, 40, 30, 10, 5, 4, 3, 2, 1, 1])

        tmp = []
        for event in filteredEvents.all():
            #Degrees to radians
            lat1=(float(A) * math.pi /180)
            long1=(float(F) * math.pi/180)
            lat2=(float(event.fi) * math.pi /180)
            long2=(float(event.lamda) * math.pi /180)

            #Calculate the distance between two points
            if(math.acos(math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(long1-long2)) * 6371 <= float(zoomlevel[int(zoom)])):
                tmp.append(event.id)

        #Get only the events in the area
        filteredEvents=filteredEvents.filter(id__in=tmp)

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
