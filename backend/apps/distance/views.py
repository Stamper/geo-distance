import json
from geopy.distance import geodesic

from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Distance
from .serializers import GeoPointSerializer, DistanceSerializer


@api_view(['GET', 'POST'])
def calculate(request):
    if request.method == 'GET':
        serializer = GeoPointSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        points = serializer.validated_data
        distance = geodesic((points['lat1'], points['lng1']), (points['lat2'], points['lng2']))
        return Response({'status': 'ok', 'data': {'km': round(distance.kilometers, 2), 'ml': round(distance.miles, 2)}})

    elif request.method == 'POST':
        serializer = DistanceSerializer(data=json.loads(request.body))
        serializer.is_valid(raise_exception=True)
        distance_data = serializer.validated_data
        Distance.objects.create(**distance_data)
        return Response(status=201)
