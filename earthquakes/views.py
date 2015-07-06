from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from earthquakes.models import stations
from django.core import serializers

def api_calls(request):

    if request.method == 'GET':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.

        #Always use get on request.POST. Correct way of querying a QueryDict.
        name = request.GET.get('name')
        code = request.GET.get('code')
        stations_list = stations.objects.filter(station_code=code)

        #need to serialize the model before sending the result of the request
        data = serializers.serialize('json', stations.objects.filter(station_code=code))

        return JsonResponse(data, safe=False)

    return render(request, 'earthquakes/index.html')
def index(request):

    stations_list = stations.objects.all().order_by('station_code')


    return render(request, 'earthquakes/index.html', { 'stations_list' : stations_list } )
