"""hollymovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from hollymovies.views import IndexView
from viewer.admin import MovieAdmin
from viewer.models import Genre, Movie

admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('viewer/', include('viewer.urls', namespace='viewer')),
    path('api-auth/', include('rest_framework.urls')),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
