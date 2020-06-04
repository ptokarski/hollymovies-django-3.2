from logging import getLogger

from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from viewer.forms import MovieForm
from viewer.models import Movie

LOGGER = getLogger()


class MovieCreateView(FormView):

    template_name = 'form.html'
    form_class = MovieForm
    success_url = reverse_lazy('movie_create')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Movie.objects.create(
            title=cleaned_data['title'],
            genre=cleaned_data['genre'],
            rating=cleaned_data['rating'],
            released=cleaned_data['released'],
            description=cleaned_data['description']
        )
        return result

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie
