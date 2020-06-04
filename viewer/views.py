from logging import getLogger

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from viewer.forms import MovieForm
from viewer.models import Movie

LOGGER = getLogger()


class MovieCreateView(CreateView):

    template_name = 'form.html'
    form_class = MovieForm
    success_url = reverse_lazy('index')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while creating a movie.')
        return super().form_invalid(form)


class MovieUpdateView(UpdateView):

    template_name = 'form.html'
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('index')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a movie.')
        return super().form_invalid(form)


class MovieDeleteView(DeleteView):
    template_name = 'movie_confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('index')


class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie
