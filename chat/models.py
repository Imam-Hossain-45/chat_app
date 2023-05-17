from django.db import models
from django.contrib.auth.models import User


class ChatWindow(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user2')

    class Meta:
        ordering = ['-id']
        unique_together = ('user1', 'user2')

    def __str__(self):
        return '{} - {}'.format(self.user1, self.user2)


class Message(models.Model):
    window = models.ForeignKey(ChatWindow, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='author')

    def __str__(self):
        return '{}:: {} ({})'.format(self.window, self.message, self.author)
