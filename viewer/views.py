from logging import getLogger

from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
)
from django.urls import reverse_lazy
from django.utils.html import escape
from django.utils.safestring import SafeString
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from hollymovies.mixins import TitleMixin
from viewer.forms import MovieForm
from viewer.models import Movie

LOGGER = getLogger()


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class MovieListView(TitleMixin, ListView):
    title = 'Movie Dashboard'
    template_name = 'movie_list.html'
    model = Movie


class MovieDetailView(LoginRequiredMixin, TitleMixin, DetailView):

    template_name = 'movie_detail.html'
    model = Movie

    def get_title(self):
        return self.object.title


class MovieCreateView(PermissionRequiredMixin, TitleMixin, CreateView):
    title = 'Add Movie'
    template_name = 'form.html'
    form_class = MovieForm
    success_url = reverse_lazy('viewer:movie_list')
    permission_required = 'viewer.add_movie'


class MovieUpdateView(
    StaffRequiredMixin, PermissionRequiredMixin, TitleMixin, UpdateView
):

    template_name = 'form.html'
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('viewer:movie_list')
    permission_required = 'viewer.change_movie'

    def get_title(self):
        safe_title = escape(self.object.title)
        return SafeString(f'Update <em>{safe_title}</em>')


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
