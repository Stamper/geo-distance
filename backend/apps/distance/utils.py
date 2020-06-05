def read_query_params(request, *args):
    return [request.GET.get(param) for param in args if param in request.GET]
