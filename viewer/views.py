from django.views.generic import ListView

from viewer.models import Movie


class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie
