from rest_framework.serializers import (
    HyperlinkedIdentityField, HyperlinkedRelatedField, ModelSerializer
)

from viewer.models import Genre, Movie


class GenreSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='viewer:genre-detail')

    class Meta:
        model = Genre
        exclude = []


class MovieSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='viewer:movie-detail')
    genre = HyperlinkedRelatedField(
        queryset=Genre.objects, view_name='viewer:genre-detail'
    )

    class Meta:
        model = Movie
        exclude = []
