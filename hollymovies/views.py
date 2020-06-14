from viewer.views import MovieListView


class IndexView(MovieListView):
    template_name = 'index.html'
