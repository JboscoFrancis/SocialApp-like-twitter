from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    post = models.TextField(max_length=2000, null=True)
    likes = models.ManyToManyField(User, related_name='likes')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    follower = models.ManyToManyField(User, blank=True, related_name='followers')

    def __str__(self):
        return str(self.user)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.png', blank=True)

    def __str__(self):
        return self.user.username