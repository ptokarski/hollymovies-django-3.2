from logging import getLogger

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
)
from django.urls import reverse_lazy
from django.utils.html import escape
from django.utils.safestring import SafeString
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_xml.renderers import XMLRenderer

from hollymovies.mixins import SuccessMessagedFormMixin, TitleMixin
from viewer.forms import MovieForm
from viewer.models import Genre, Movie
from viewer.serializers import (
    GenreSerializer, MovieSerializer, MovieShortSerializer
)

LOGGER = getLogger()


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects
    serializer_class = GenreSerializer
    renderer_classes = APIView.renderer_classes + [XMLRenderer]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class MovieViewSet(ModelViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    class pagination_class(PageNumberPagination):
        page_query_param = 'p'
        page_size = 10
        page_size_query_param = 'per_page'

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieShortSerializer
        return super().get_serializer_class()


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class MovieListView(TitleMixin, ListView):
    title = 'Movie Dashboard'
    template_name = 'movie_list.html'
    model = Movie
    paginate_by = 20


class MovieDetailView(LoginRequiredMixin, TitleMixin, DetailView):

    template_name = 'movie_detail.html'
    model = Movie

    def get_title(self):
        return self.object.title


class MovieCreateView(
    PermissionRequiredMixin, TitleMixin, SuccessMessagedFormMixin, CreateView
):

    title = 'Add Movie'
    template_name = 'form.html'
    form_class = MovieForm
    success_url = reverse_lazy('viewer:movie_list')
    permission_required = 'viewer.add_movie'

    def get_success_message(self):
        safe_title = escape(self.object.title)
        return SafeString(f'Movie <strong>{safe_title}</strong> added!')


class MovieUpdateView(
    StaffRequiredMixin, PermissionRequiredMixin,
    TitleMixin, SuccessMessagedFormMixin, UpdateView
):

    template_name = 'form.html'
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('viewer:movie_list')
    permission_required = 'viewer.change_movie'

    def get_title(self):
        safe_title = escape(self.object.title)
        return SafeString(f'Update <em>{safe_title}</em>')

    def get_success_message(self):
        safe_title = escape(self.object.title)
        return SafeString(f'Movie <strong>{safe_title}</strong> updated!')


class MovieDeleteView(
    StaffRequiredMixin, PermissionRequiredMixin, TitleMixin, DeleteView
):

    template_name = 'movie_confirm_delete.html'
    model = Movie
    permission_required = 'viewer.delete_movie'
    success_url = reverse_lazy('viewer:movie_list')

    def test_func(self):
        return super().test_func() and self.request.user.is_superuser

    def get_title(self):
        safe_title = escape(self.object.title)
        return SafeString(f'Delete <em>{safe_title}</em>')

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        safe_title = escape(self.object.title)
        message = SafeString(f'Movie <strong>{safe_title}</strong> removed.')
        messages.success(request, message)
        return result
