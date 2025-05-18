from django.db import models
from django.db.models import UniqueConstraint
from django.conf import settings

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        db_table = "tag"
        constraints = [
            UniqueConstraint(fields=['name', 'user'], name='unique_tag_per_user')
        ]

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='notes')
    is_archived = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        db_table = "note"