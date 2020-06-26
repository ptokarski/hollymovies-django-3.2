from django.urls import include, path
from rest_framework.routers import DefaultRouter

from viewer.views import (
    GenreViewSet, MovieCreateView, MovieDeleteView, MovieDetailView,
    MovieListView, MovieUpdateView
)

router = DefaultRouter()
router.register('genre', GenreViewSet)

app_name = 'viewer'
urlpatterns = [
    path('movie/list', MovieListView.as_view(), name='movie_list'),
    path('movie/detail/<pk>', MovieDetailView.as_view(), name='movie_detail'),
    path('movie/create', MovieCreateView.as_view(), name='movie_create'),
    path('movie/update/<pk>', MovieUpdateView.as_view(), name='movie_update'),
    path('movie/delete/<pk>', MovieDeleteView.as_view(), name='movie_delete'),
    path('api/', include(router.urls))
]
