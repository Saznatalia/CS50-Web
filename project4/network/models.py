from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False, related_name='related_to')
    profile_img = models.ImageField(default="default.jpg", upload_to="profile_pic")

    def add_relationship(self, user):
        relationship = Relationship.objects.get_or_create(
            from_user = self,
            to_user = user
        )
        return relationship

    def delete_relationship(self, user):
        Relationship.objects.filter(
            from_user = self,
            to_user = user).delete()
        return

    def get_following(self):
        return self.relationships.filter(to_user__from_user=self)
    
    def get_followers(self):
        return self.related_to.filter(from_user__to_user=self)
    
    def __str__(self):
        return f"{self.user}"

class Relationship(models.Model):
    from_user = models.ForeignKey(Profile, related_name='from_user', on_delete=models.DO_NOTHING)
    to_user = models.ForeignKey(Profile, related_name='to_user', on_delete=models.DO_NOTHING)


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author')
    post_date = models.DateTimeField(default=datetime.now)
    content = models.TextField()
    likes = models.ManyToManyField(Profile, blank=True, related_name='likes')

    def get_total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.author}: on {self.post_date} posted {self.content} with {self.likes}"