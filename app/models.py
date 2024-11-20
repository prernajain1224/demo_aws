from django.db import models
from django.contrib.auth.models import User
import uuid


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DEPARTMENT_CHOICES = [
        ('data', 'Data'),
        ('infra', 'Infrastructure'),
        ('digital_marketing', 'Digital Marketing'),
    ]
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.department}"
