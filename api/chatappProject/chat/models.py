from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission


class User(AbstractUser):
    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(Group, related_name='chat_users', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='chat_users', blank=True
    )

class Channel(models.Model):
    name = models.CharField(max_length=60)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channels_from')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channels_to')


class Message(models.Model):
    message = models.TextField()
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_from')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_to')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
