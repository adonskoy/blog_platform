from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q


class PostManager(models.Manager):
    def personal_feed(self, user: get_user_model()):
        posts = super().get_queryset().filter(
            Q(author=user) | Q(author__in=user.subscriptions.all())
        )

        return posts.order_by("-date_published")

    def feed(self):
        posts = super().get_queryset().all()
        return posts.order_by("-date_published")
