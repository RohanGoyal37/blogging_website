from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Category
from .forms import RegisterForm, PostForm, CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Main page view - shows all blog posts
def index(request):
    # Get all posts, newest first
    posts = Post.objects.all().order_by('-created_at')
    # Get categories for the sidebar
    categories = Category.objects.all()
    return render(request, 'blogs/index.html', {
        'posts': posts, 
        'categories': categories
    })

# Single post page with comments
def post_detail(request, pk):
    # Find the post or show 404 if not found
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    # Handle new comment submission
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            # Save comment but set post and user first
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blogs/post_detail.html', {
        'post': post, 
        'comments': comments, 
        'form': form
    })

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'blogs/register.html', {'form': form})

# Only logged-in users can create posts
@login_required
def post_create(request):
    if request.method == "POST":
        # Handle both text and file data (for images)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Create post but don't save yet
                post = form.save(commit=False)
                post.author = request.user  # Set the current user as author
                
                # Figure out which category to use
                category_choice = form.cleaned_data.get('category')
                if category_choice == 'other':
                    new_cat_name = form.cleaned_data.get('new_category')
                    if new_cat_name:
                        category, created = Category.objects.get_or_create(name=new_cat_name)
                        post.category = category
                else:
                    category = Category.objects.get(id=int(category_choice))
                    post.category = category

                post.save()
                return redirect('post_detail', pk=post.pk)
            except Exception as e:
                print(f"Error saving post: {e}")
                form.add_error(None, "Error saving the post. Please try again.")
    else:
        form = PostForm()
    return render(request, 'blogs/post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=post.pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)

            # Handle new category creation
            new_cat_name = form.cleaned_data.get('new_category')
            if new_cat_name:
                category, created = Category.objects.get_or_create(name=new_cat_name)
                post.category = category

            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blogs/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST" and request.user == post.author:
        post.delete()
        return redirect('index')
    return redirect('post_detail', pk=pk)

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.user:
        post_pk = comment.post.pk
        comment.delete()
        return redirect('post_detail', pk=post_pk)
    return redirect('post_detail', pk=comment.post.pk)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'blogs/category_posts.html', {
        'category': category,
        'categories': categories,
        'posts': posts
    })

def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(title__icontains=query) | \
                Post.objects.filter(content__icontains=query)
    else:
        posts = Post.objects.none()
    
    categories = Category.objects.all()
    return render(request, 'blogs/search_results.html', {
        'posts': posts,
        'query': query,
        'categories': categories
    })

@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))

@login_required
def toggle_bookmark(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.bookmarks.all():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))
