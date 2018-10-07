from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .managers import PostManager


# Create your models here.


class Post(models.Model):
    objects = PostManager()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_published = models.DateTimeField()
    tittle = models.CharField(max_length=256)
    content = models.TextField()

    def __str__(self):
        return self.tittle

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_writen = models.DateTimeField()
    text = models.TextField()
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    def has_childs(self):
        return bool(self.all_childs().count())

    def all_childs(self):
        return Comment.objects.filter(reply_to=self, post=self.post)
