from django.urls import path

from viewer.views import (
    IndexView, MovieCreateView, MovieDeleteView, MovieDetailView,
    MovieListView, MovieUpdateView
)

app_name = 'viewer'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('movie/list', MovieListView.as_view(), name='movie_list'),
    path('movie/detail/<pk>', MovieDetailView.as_view(), name='movie_detail'),
    path('movie/create', MovieCreateView.as_view(), name='movie_create'),
    path('movie/update/<pk>', MovieUpdateView.as_view(), name='movie_update'),
    path('movie/delete/<pk>', MovieDeleteView.as_view(), name='movie_delete')
]
