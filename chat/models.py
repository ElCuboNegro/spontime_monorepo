from django.db import models
from django.conf import settings


class Message(models.Model):
    """Chat messages for plans."""
    plan = models.ForeignKey(
        'plans.Plan',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.handle or self.user.username}: {self.content[:50]}"

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['plan', 'created_at']),
        ]

