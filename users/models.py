from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    class Meta:
        permissions = (("can_delete_post", "Can delete a post"),
                       ("can_delete_comment", "Can delete a comment"),
                       ("can_ban_user", "Can ban a user"),)