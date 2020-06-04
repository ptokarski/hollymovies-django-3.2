from django.views.generic import TemplateView

from viewer.models import Movie


class MoviesView(TemplateView):
    template_name = 'movies.html'
    extra_context = {'movies': Movie.objects.all()}
