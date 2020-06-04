from django.views.generic import FormView, ListView

from viewer.forms import MovieForm
from viewer.models import Movie


class MovieCreateView(FormView):
    template_name = 'form.html'
    form_class = MovieForm


class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie
