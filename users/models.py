from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="biography")
    is_private = models.BooleanField(default=False, verbose_name="Private profile")

    class Meta:
        permissions = (("can_delete_post", "Can delete a post"),
                       ("can_delete_comment", "Can delete a comment"),
                       ("can_ban_user", "Can ban a user"),)

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"