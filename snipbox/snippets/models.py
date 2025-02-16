from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    title = models.CharField(max_length = 100, null = False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class Snippet(models.Model):
    title = models.CharField(max_length = 255, null = False)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    tags = models.ManyToManyField(Tag, blank = True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Order by newest first