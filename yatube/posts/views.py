from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page

# Create your views here.
from .models import Post, Group, Follow
from .forms import PostForm, CommentForm


User = get_user_model()


@cache_page(20)
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page,
                                          'paginator': paginator})


def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('index')
        return render(request, 'new.html', {'form': form})
    form = PostForm()
    return render(request, 'new.html', {'form': form})


def profile(request, username):
        profile = get_object_or_404(User, username=username)
        posts = Post.objects.filter(author=profile).all()
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        try:
            f = get_object_or_404(Follow, user=request.user, author=profile)
            following = True
        except:
            following = False
        context = {'profile': profile, 'page': page, 'paginator': paginator,
                    'following': following}
        return render(request, 'profile.html', context)
 
 
def post_view(request, username, post_id):
        profile = get_object_or_404(User, username=username)
        post = Post.objects.get(pk=post_id)
        items = post.comments.all()
        form = CommentForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.instance.author = request.user
                form.instance.post = post
                form.save()
                return redirect('post', post.author.username, post.pk)
        return render(request, 'post.html',
                      {'profile': profile, 'post': post,
                       'form': form, 'items': items})


def post_edit(request, username, post_id):
        post = Post.objects.get(pk=post_id)
        if request.user == post.author:
            form = PostForm(request.POST or None, instance=post,
                            files=request.FILES or None)
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    return redirect('post', post.author.username, post.pk)
            return render(request, 'new.html', {'form': form})
        
        return redirect('post', post.author.username, post.pk)


def follow_index(request):
    # с помощью метода values_list('author') создается запрос QuerySet в базу
    # данных, который соберет id авторов, на которых подписан юзер
    authors = User.objects.get(pk = request.user.pk).follower.all(
                                            ).values_list('author')
    posts = Post.objects.filter(author__in=authors)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page, 'paginator': paginator})


def profile_follow(request, username):
    author = User.objects.get(username=username)
    Follow.objects.create(user=request.user, author=author)
    return redirect('profile', username)


def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    follow = Follow.objects.get(user=request.user, author=author)
    follow.delete()
    return redirect('profile', username)


def page_not_found(request, exeption):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


'''def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    profile = get_object_or_404(User, username=username)
    # items = Comment.objects.filter(post=post).all()
    items = post.comments.all().order_by('-created')
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post = post
            form.save()
            return redirect('post', post.author.username, post.pk)
    return render(request, 'post.html',
                  {'profile': profile, 'post': post,
                   'form': form, 'items': items})'''
