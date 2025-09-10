from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    # Store categories like Tech, Lifestyle, etc.
    name = models.CharField(max_length=50)
    # URL-friendly version of the name
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-generate the slug from category name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    # Basic post info
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    
    # Timestamps for tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional fields
    excerpt = models.TextField(blank=True, null=True)  # Short preview text
    featured_image = models.ImageField(
        upload_to="posts/", 
        blank=True, 
        null=True,
        help_text="Cover image for your post"
    )
    
    # Interaction tracking
    likes = models.ManyToManyField(
        User, 
        related_name="liked_posts", 
        blank=True
    )
    bookmarks = models.ManyToManyField(
        User, 
        related_name="bookmarked_posts", 
        blank=True
    )

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()

    def total_bookmarks(self):
        return self.bookmarks.count()

    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
