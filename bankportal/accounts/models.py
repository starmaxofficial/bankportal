from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def statement_upload_path(instance, filename):
    return f'statements/user_{instance.user.id}/{filename}'

class Statement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statements')
    title = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to=statement_upload_path)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
