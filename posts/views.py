import operator
from . forms import PostForm
from . models import Post
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()


def index(request):
    if request.user.is_authenticated:
        posts = []
        user_posts = Post.objects.filter(user=request.user)
        all_users = User.objects.all().exclude(id=request.user.id)
        connections = [user for user in request.user.connection.all()]
        non_connections = [
            user for user in all_users if user not in connections]
        for post in user_posts:
            posts.append(post)
        for connection in connections:
            connection_posts = Post.objects.filter(user=connection)
            for post in connection_posts:
                posts.append(post)
        for non_connection in non_connections:
            non_connection_posts = Post.objects.filter(
                user=non_connection, is_public=True)
            for post in non_connection_posts:
                posts.append(post)
        if len(posts) > 0:
            posts = sorted(posts, reverse=True,
                           key=operator.attrgetter('updated_date'))
        users = non_connections
    else:
        posts = Post.objects.filter(is_public=True).order_by('-updated_date')
        users = User.objects.all()
    context = {
        'posts': posts,
        'users': users
    }
    return render(request, 'posts/index.html', context=context)


@ login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data['picture']
            content = form.cleaned_data['content']
            is_public = form.cleaned_data['is_public']
            post = Post(picture=picture, content=content,
                        is_public=is_public, user=request.user)
            post.save()
            messages.success(request, 'New Post Created')
            return redirect('index')
        else:
            messages.error(request, 'Something went wrong!! Please try again')
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/new_post.html', context=context)


@login_required
def edit_post(request, id):
    post = Post.objects.filter(id=id).first()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['picture']:
                post.picture = form.cleaned_data['picture']
            post.content = form.cleaned_data['content']
            post.is_public = form.cleaned_data['is_public']
            post.save()
            messages.success(request, 'Post Edited')
            return redirect('index')
        else:
            messages.error(request, 'Something went wrong!! Please try again')
    else:
        form_data = {
            'picture': post.picture,
            'content': post.content,
            'is_public': post.is_public,
        }
        form = PostForm(initial=form_data)
    context = {
        'form': form,
    }
    return render(request, 'posts/edit_post.html', context=context)


@login_required
def delete_post(request, id):
    post = Post.objects.filter(id=id).first()
    post.delete()
    messages.success(request, 'Post Deleted')
    return redirect('index')


@login_required
def like_post(request):
    if request.is_ajax():
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id=post_id)
        updated = False
        liked = False
        if request.user in post.get_likes():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        updated = True
        total_likes = Post.objects.get(id=post_id).get_likes_count()
        data = {
            'updated': updated,
            'liked': liked,
            'total_likes': total_likes,
        }
        return JsonResponse({'data': data})
    return JsonResponse({})


def lightbox(request):
    return render(request, 'posts/lightbox.html')


def error_404(request,  exception):
    return render(request, '404.html')
