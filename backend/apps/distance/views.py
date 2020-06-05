import json
from geopy.distance import geodesic
from .models import Distance
from .utils import read_query_params
from .serializers import DistanceSchema, ValidationError

from django.http import JsonResponse, HttpResponse


def calculate(request):
    if request.method == 'GET':
        error = False
        params_list = ('lat1', 'lng1', 'lat2', 'lng2')
        params = read_query_params(request, *params_list)
        if len(params) != len(params_list):
            error = True

        try:
            distance = geodesic((params[0], params[1]), (params[2], params[3]))

        except (ValueError, IndexError):
            error = True

        if error:
            resp = JsonResponse({'status': 'error'})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp

        else:
            resp = JsonResponse({'status': 'ok', 'data': {'km': round(distance.kilometers, 2), 'ml': round(distance.miles, 2)}})
            resp['Access-Control-Allow-Origin'] = '*'
            return resp

    elif request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))
        try:
            distance_data = DistanceSchema().load(payload)
            Distance.objects.create(**distance_data)

            return HttpResponse(status=201)

        except ValidationError:
            return HttpResponse(status=400)
