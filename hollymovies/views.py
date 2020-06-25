from viewer.views import MovieListView


class IndexView(MovieListView):
    title = 'Welcome to HollyMovies!'
    template_name = 'index.html'
