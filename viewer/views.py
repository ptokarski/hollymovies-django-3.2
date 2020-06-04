from django.shortcuts import render

from viewer.models import Movie


def movies(request):
    return render(
        request, template_name='movies.html',
        context={'movies': Movie.objects.all()}
    )
