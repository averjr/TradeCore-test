from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(null=True)

    likes = models.ManyToManyField(User, blank=True, related_name='liked')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    @property
    def number_of_likes(self):
        return self.likes.count()
