from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(null=True)

    liked_by = models.ManyToManyField(User, blank=True, related_name='liked')

    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='posts')

    @property
    def number_of_likes(self):
        return self.likes.count()

    @property
    def is_liked_by_me(self):
        # TODO: check https://stackoverflow.com/questions/52219902/how-to-safely-access-request-object-in-django-models
        # to get right value
        return None
