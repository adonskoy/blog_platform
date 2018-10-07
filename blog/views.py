from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from blog.models import Post, Comment


# Create your views here.


def feed(request):
    posts = Post.objects.feed()
    return render(request, "feed.html", {"posts": posts})


@login_required
def personal_feed(request):
    posts = Post.objects.personal_feed(request.user)
    return render(request, "feed.html", {"posts": posts})


def post(request, pk):
    try:
        post = Post.objects.get(pk=id)
    except:
        return HttpResponseNotFound("404")

    comments = Comment.objects.filter(post=post, reply_to=None)

    return render(request, "post.html", {"post": post, "comments": comments})
