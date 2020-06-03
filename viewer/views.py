from django.http import HttpResponse


def hello(request, s0):
    s1 = request.GET['s1']
    return HttpResponse(f'Hello, {s0} and {s1} world!')
