from .models import Post, Group
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from functools import wraps


LIMIT: int = 10


def authorized_only(func):
    @wraps(func)
    def check_user(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return redirect('/auth/login/')
    return check_user


@authorized_only
def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@authorized_only
def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:LIMIT]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
