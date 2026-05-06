from django.db import models
from django.conf import settings

class ChatSession(models.Model):
    TOPIC_CHOICES = [
        ('tax', 'Tax & ITR'),
        ('investment', 'Investments'),
        ('gst', 'GST'),
        ('planning', 'Financial Planning'),
        ('general', 'General'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES, default='general')
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_display_name()} - {self.topic} - {self.created_at.strftime('%d %b')}"

class ChatMessage(models.Model):
    ROLE_CHOICES = [('user', 'User'), ('assistant', 'AI CA')]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
