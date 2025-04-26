from django.db import models
from user_mgmt.models import User

class CommentTarget(models.TextChoices):
    LISTING = 'listing', 'Listing'
    BLOG = 'blog', 'Blog'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class BlogPost(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    posting_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['posting_date']),
        ]

class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    target_type = models.CharField(
        max_length=10,
        choices=CommentTarget.choices
    )
    target_id = models.IntegerField()
    content = models.TextField()
    posting_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} on {self.target_type}"

    class Meta:
        indexes = [
            models.Index(fields=['target_type', 'target_id']),
            models.Index(fields=['posting_date']),
        ] 