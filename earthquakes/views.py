from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from earthquakes.models import stations, events
from django.core import serializers
from time import time,strftime
import datetime
import time
import pytz
from array import *
import datetime,math,cmath
from pymongo import MongoClient
from json import JSONEncoder
from bson.json_util import dumps
import json
from chartit import DataPool, Chart
from guralp.models import guralp,history
from graphos.sources.mongo import MongoDBDataSource
from graphos.sources.simple import SimpleDataSource
import numpy as np
import csv
from graphos.renderers import gchart

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
        includeMap = request.GET.get('includeMap')

        filteredStations=stations.objects.filter(station_name__icontains=name)\
        .filter(station_code__startswith=code.upper())\
        .filter(height__icontains=height) \
        .filter(soil_class__icontains=soilClass) \
        .filter(owner__icontains=owner)

        if vs30High and vs30Low:
            filteredStations=filteredStations.filter(vs30__gte=vs30Low, vs30__lte=vs30High)
        elif vs30High and not vs30Low:
            filteredStations=filteredStations.filter(vs30__lte=vs30High)
        elif vs30Low and not vs30High:
            filteredStations=filteredStations.filter(vs30__gte=vs30Low)

        #If includeMap is selected then process for stations around the area
        if includeMap == "true":
            #Distance (in km from the center of the map to the edges
            zoomlevel = array("i",[1000000, 100000, 10000 , 1000 , 600, 500 , 400 ,300 , 170, 100, 70, 50, 30, 20, 10, 5, 4, 3, 2, 1, 1, 1])

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
        includeMap = request.GET.get('includeMap')

        dt=datetime.datetime.strptime(eventStartDate, "%a %b %d %Y").date()
        dtt=datetime.datetime.strptime(eventEndDate, "%a %b %d %Y").date()
        filteredEvents = events.objects.all()

        if eventID:
            filteredEvents = filteredEvents.filter(event_id__icontains=eventID)

        if eventStartDate and eventEndDate:
            filteredEvents = filteredEvents.filter(datetime__range=[dt, dtt])

        if eventLowDepth and eventHighDepth:
            filteredEvents = filteredEvents.filter(depth__gte=eventLowDepth, depth__lte=eventHighDepth)
        elif eventLowDepth and not eventHighDepth:
            filteredEvents = filteredEvents.filter(depth__gte=eventLowDepth)
        elif eventHighDepth and not eventLowDepth:
            filteredEvents = filteredEvents.filter(depth__lte=eventHighDepth)

        if eventLowMMF and eventHighMMF:
            filteredEvents = filteredEvents.filter(mmf__gte=eventLowMMF, mmf__lte=eventHighMMF)
        elif eventLowMMF and not eventHighMMF:
            filteredEvents = filteredEvents.filter(mmf__gte=eventLowMMF)
        elif eventHighMMF and not eventLowMMF:
            filteredEvents = filteredEvents.filter(mmf__lte=eventHighMMF)

        if includeMap == "true":
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

def get_filenames_datetime_range(request):
    try:
        client = MongoClient()
        db = client.test_database
    except:
        print "Couldn't connect to mongoDB database"

    try:
        collection = db.files
    except:
        print "Couldn't retreive files collection"


    if request.method == 'GET':
        eventStartDate = request.GET.get('eventStartDate')
        eventEndDate = request.GET.get('eventEndDate')
        try:
            start = strftime("%Y-%m-%dTH",time.strptime(eventStartDate,"%a %b %d %Y"))
            end = strftime("%Y-%m-%dTH",time.strptime(eventEndDate,"%a %b %d %Y"))
            files_collection = collection.find({ "dateTime": { "$gte" : start, "$lte": end }}, {"file_name": 1 })
        except Exception,e:
            print e

        try:
            #parsing pymongo Cursor to dict
            objects = []
            for single_file in files_collection:
                objects.append(single_file)

        except Exception,e:
            print e

        try:
            #dict to json
            json_string = dumps(objects)
        except Exception,e:
            print e

        return JsonResponse(json_string, safe=False)




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

def plotting_files(request):
    if request.GET:
        try:
            get_datetime = request.GET['datetime']
        except Exception,e:
            print "Couldn't retreive datetime from GET",e

        try:
            client = MongoClient()
            db = client.test_database
        except Exception,e:
            print "Couldn't connect to mongoDB database"

        try:
            collection = db.files
        except Exception,e:
            print e

        try: #construct datetime from string
            received_datetime = datetime.datetime.strptime(get_datetime, "%Y-%m-%dT%H:%M:%SZ")

        except Exception,e:
            print "Couldn't parse date",e

        try:
            start_date = received_datetime + datetime.timedelta(hours=1)
            new_start_date = start_date.strftime("%Y-%m-%dTH%H:%M:%SZ")
            end_date = received_datetime + datetime.timedelta(hours=-1)
            new_end_date = end_date.strftime("%Y-%m-%dTH%H:%M:%SZ")

        except Exception,e:
            print "Couldn't calculate start and end dates",e
        try:
            files_collection = collection.find({ "dateTime": { "$gte" : new_end_date, "$lte": new_start_date }}, {"file_name" : 1 })

            if request.GET['pr'] == "true" and request.GET['un'] == "true" and request.GET['sp'] == "true":
                files_collection = collection.find({ "station": station_code }, {"file_name" : 1 })
                print "FULLEXTEA"
            elif request.GET['pr'] == "true" and request.GET['un']:
                print "nai"
                files_collection = collection.find({ "$and" : [ { "dateTime": { "$gte" : new_end_date, "$lte": new_start_date }}, { "type" : "unprocessed"}, { "type" : "processed"}] },{"file_name" : 1 })
                #files_collection = collection.find({ "station": station_code, "type" : "processed"}, {"file_name" : 1 })
            elif request.GET['pr'] == "true" and request.GET['sp']:
                files_collection = collection.find({ "$and" : [ { "dateTime": { "$gte" : new_end_date, "$lte": new_start_date }}, { "type" : "spectra"}, { "type" : "processed"}] },{"file_name" : 1 })
            elif request.GET['un'] == "true" and request.GET['un']:
                files_collection = collection.find({ "$and" : [ { "dateTime": { "$gte" : new_end_date, "$lte": new_start_date }}, { "type" : "unprocessed"}, { "type" : "spectra"}] },{"file_name" : 1 })
            elif request.GET['un'] == "true":
                files_collection = collection.find({ "$and" : [ { "dateTime": { "$gte" : new_end_date, "$lte": new_start_date }}, { "type" : "unprocessed"}] },{"file_name" : 1 })
            elif request.GET['pr'] == "true":
                files_collection = collection.find({ "$and" : [ { "dateTime": { "$gte" : new_end_date, "$lte": new_start_date }}, { "type" : "processed"}] },{"file_name" : 1 })
            elif request.GET['sp'] == "true":
                files_collection = collection.find({ "$and" : [ { "dateTime": { "$gte" : new_end_date, "$lte": new_start_date }}, { "type" : "spectra"}] },{"file_name" : 1 })

        except Exception,e:
            print e

    return render(request, 'earthquakes/plot.html', { 'files' : files_collection, 'datetime' : get_datetime } )
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def chart(request):


    if request.GET:
        try:
            file_name = request.GET['id']
        except Exception,e:
            print "Couldn't retreive file name from GET",e

        try:
            client = MongoClient()
            db = client.test_database
        except Exception,e:
            print "Couldn't connect to mongoDB database"

        try:
            collection = db.files
        except Exception,e:
            print e

        ic=collection.find_one({"file_name" : file_name })


        if ic["status"] == "spectra":

            data_fr,data_sd =  [],[]
            counter=0

            for c in ic["data"]:
                first,second,third = c.split()
                counter+=1
                if is_number(first) and is_number(second) and is_number(third):
                    data_fr.append([float(first), float(second)])
                    data_sd.append([float(first), float(third)])
                elif counter==1:
                    data_fr.append([first,second])
                    data_sd.append([first,third])

            for c in data_fr:
                print c
            chart_fr = gchart.LineChart(SimpleDataSource(data=data_fr))
            chart_sd = gchart.LineChart(SimpleDataSource(data=data_sd))




            return render(request, 'earthquakes/chart_multiple.html', { 'chart_fr' : chart_fr , 'chart_sd' : chart_sd } )




        else:

            data  =  []

            ic=collection.find_one({"file_name" : file_name })
            counter=0
            for c in ic["data"]:
                first,second= c.split()
                counter+=1
                #check if the data retreived ar numbers
                if is_number(first) and is_number(second):
                    data.append([float(first), float(second)])
                #if there are not numbers, check if they are labels
                elif counter==1:
                    data.append([first, second])
                #data are not consistened
                else:
                    return render(request, 'earthquakes/404f.html')


            chart = gchart.LineChart(SimpleDataSource(data=data))
            for c in data:
                print c

            return render(request, 'earthquakes/chart.html', { 'point_chart' : chart } )

def plotting_station_files(request):
    if request.GET:
        try:
            station_code = request.GET['code']
        except Exception,e:
            print "Couldn't retreive datetime from GET",e

        try:
            client = MongoClient()
            db = client.test_database
        except Exception,e:
            print "Couldn't connect to mongoDB database"

        try:
            collection = db.files
        except Exception,e:
            print e
        try:
            files_collection = collection.find({ "station": station_code }, {"file_name" : 1 })
            if request.GET['pr'] == "true" and request.GET['un'] == "true" and request.GET['sp'] == "true":
                files_collection = collection.find({ "station": station_code }, {"file_name" : 1 })
            elif request.GET['pr'] == "true" and request.GET['un']:
                files_collection = collection.find({ "$and" : [ {"station": station_code }, { "type" : "unprocessed"}, { "type" : "processed"}] },{"file_name" : 1 })
                #files_collection = collection.find({ "station": station_code, "type" : "processed"}, {"file_name" : 1 })
            elif request.GET['pr'] == "true" and request.GET['sp']:
                files_collection = collection.find({ "$and" : [ {"station": station_code }, { "type" : "spectra"}, { "type" : "processed"}] },{"file_name" : 1 })
            elif request.GET['un'] == "true" and request.GET['un']:
                files_collection = collection.find({ "$and" : [ {"station": station_code }, { "type" : "unprocessed"}, { "type" : "spectra"}] },{"file_name" : 1 })
            elif request.GET['un']:
                files_collection = collection.find({ "$and" : [ {"station": station_code }, { "type" : "unprocessed"}] },{"file_name" : 1 })
            elif request.GET['pr']:
                files_collection = collection.find({ "$and" : [ {"station": station_code }, { "type" : "processed"}] },{"file_name" : 1 })
            elif request.GET['sp']:
                files_collection = collection.find({ "$and" : [ {"station": station_code }, { "type" : "spectra"}] },{"file_name" : 1 })



        except Exception,e:
            print e


        return render(request, 'earthquakes/plot_station.html', { 'files' : files_collection, 'station_code' : station_code } )

def download_files(request):


    response = HttpResponse(content_type='text')
    response['Content-Disposition'] = 'attachment; filename="ABS1_19950513084713.L.dat.smc8.alc00.129ns08.taper__0.0__0.0.d.asc"'

    writer = csv.writer(response)
    writer.writerow(['First rowBaz'])
    writer.writerow(['Second rowHeres a quote'])

    return response
