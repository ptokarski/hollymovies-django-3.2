from logging import getLogger

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from viewer.forms import MovieForm
from viewer.models import Movie

LOGGER = getLogger()


class MovieListView(ListView):
    template_name = 'movie_list.html'
    model = Movie


class MovieDetailView(DetailView):
    template_name = 'movie_detail.html'
    model = Movie


class MovieCreateView(CreateView):
    template_name = 'form.html'
    form_class = MovieForm
    success_url = reverse_lazy('viewer:movie_list')


class MovieUpdateView(UpdateView):
    template_name = 'form.html'
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('viewer:movie_list')


class MovieDeleteView(DeleteView):
    template_name = 'movie_confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('viewer:movie_list')


class IndexView(MovieListView):
    template_name = 'index.html'
