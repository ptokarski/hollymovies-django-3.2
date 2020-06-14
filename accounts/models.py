from django.contrib.auth.models import User
from django.db.models import CASCADE, Model, OneToOneField, TextField


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    biography = TextField()
