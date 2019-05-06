from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.contrib import messages
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator

# Create your views here.
def home(request): #request란? 사용자가 요청한 메서드 + string + ... 값 / 해쉬 형태로 넘어간다
    post_list = Post.objects.all().order_by('-updated_at')
    paginator = Paginator(post_list, 10)

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'blog/home.html', {'posts' : posts})

def detail(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/detail.html', {'post': post_detail})

def comment_new(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        # post = get_object_or_404(Post)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = Post.objects.get(pk=pk)
            comment.save()
            return redirect("blog.views.detail", pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_new.html', {'form': form})

def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('detail', post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/new.html', {'form': form})

def edit(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(request.POST, instance = post)
        if form.is_valid():
            form.save()
            return redirect('detail', post.pk)
    else:
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(instance = post)
    return render(request, 'blog/edit.html', {'form': form, 'post': post})

def remove(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('home')
