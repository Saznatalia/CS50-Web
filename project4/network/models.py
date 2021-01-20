from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    post_date = models.DateTimeField(default=datetime.now())
    post = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return f"{self.user}: on {self.post_date} posted {self.post}"