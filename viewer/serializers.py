from rest_framework.serializers import (
    HyperlinkedIdentityField, ModelSerializer
)

from viewer.models import Genre


class GenreSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='viewer:genre-detail')

    class Meta:
        model = Genre
        exclude = []
