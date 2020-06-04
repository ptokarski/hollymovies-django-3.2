from logging import getLogger

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from viewer.forms import MovieForm
from viewer.models import Movie

LOGGER = getLogger()


class MovieCreateView(CreateView):

    template_name = 'form.html'
    form_class = MovieForm
    success_url = reverse_lazy('movie_create')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie
