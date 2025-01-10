from django.db import models
from user.models import User
from django.utils.timezone import now


class Task(models.Model):
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    completed = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def save(self, *args, **kwargs):
        if not self.is_active and self.completed is None:
            self.completed = now()
        elif self.is_active:
            self.completed = None

        super().save(*args, **kwargs)