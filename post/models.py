from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Post(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=60, blank=False, null=False)
    description = models.TextField(max_length=250, null=False, blank=False)
    time = models.DateTimeField(default=datetime.now(), null=False, blank=False)
    image = models.ImageField(upload_to='images/posts/', null=True, blank=True)

    def __str__(self):
        return f'ID: {self.pk}, Title: {self.title}, Uploader: {self.uploader.username}'

