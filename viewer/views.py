from logging import getLogger

from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
)
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from viewer.forms import MovieForm
from viewer.models import Movie

LOGGER = getLogger()


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class MovieListView(ListView):
    template_name = 'movie_list.html'
    model = Movie


class MovieDetailView(LoginRequiredMixin, DetailView):
    template_name = 'movie_detail.html'
    model = Movie


class MovieCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = MovieForm
    success_url = reverse_lazy('viewer:movie_list')
    permission_required = 'viewer.add_movie'


class MovieUpdateView(
    StaffRequiredMixin, PermissionRequiredMixin, UpdateView
):
    template_name = 'form.html'
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('viewer:movie_list')
    permission_required = 'viewer.change_movie'


class MovieDeleteView(
    StaffRequiredMixin, PermissionRequiredMixin, DeleteView
):

    template_name = 'movie_confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('viewer:movie_list')
    permission_required = 'viewer.delete_movie'

    def test_func(self):
        return super().test_func() and self.request.user.is_superuser
