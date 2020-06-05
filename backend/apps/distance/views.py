from geopy.distance import geodesic
from .utils import read_query_params

from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def calculate(request):
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
