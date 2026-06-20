from django.db import models

from users.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    is_pinned = models.BooleanField(default=False, verbose_name="Pinned")


    class Meta:
        ordering = ['-created_at']

    @property
    def is_news(self):
        return hasattr(self, 'news')

    def __str__(self):
        return f"Post di {self.author.username} del {self.created_at.strftime('%d/%m/%Y')}"


class News(Post):
    title = models.CharField(max_length=200)
    source = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"News: {self.title}"



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment written by {self.author.username} on {self.post.id}"