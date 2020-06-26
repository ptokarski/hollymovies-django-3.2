from rest_framework.serializers import (
    HyperlinkedIdentityField, HyperlinkedRelatedField, ModelSerializer
)

from viewer.models import Genre, Movie


class GenreSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='viewer:genre-detail')

    class Meta:
        model = Genre
        exclude = []


class MovieShortSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='viewer:movie-detail')
    genre = GenreSerializer()

    class Meta:
        model = Movie
        fields = ['url', 'title', 'genre', 'released', 'rating']


class MovieSerializer(ModelSerializer):

    genre = HyperlinkedRelatedField(
        queryset=Genre.objects, view_name='viewer:genre-detail'
    )

    class Meta:
        model = Movie
        exclude = []
