from django.forms import (
    CharField, DateField, Form, IntegerField, ModelChoiceField, Textarea
)

from viewer.models import Genre


class MovieForm(Form):
    title = CharField(max_length=128)
    genre = ModelChoiceField(queryset=Genre.objects)
    rating = IntegerField(min_value=1, max_value=10)
    released = DateField()
    description = CharField(widget=Textarea, required=False)
