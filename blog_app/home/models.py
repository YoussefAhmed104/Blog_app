from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=200)
    auther = models.ForeignKey(User ,on_delete=models.CASCADE , related_name= 'blog_post',null=True , blank=True)
    body = models.TextField()
    publish = models.DateField(default=timezone.now)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)

    class Meta:
        ordering = ['-publish']  #to order the posts from oldest to newest 
        indexes =[
            models.Index(fields=['publish']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:details", args=[self.id])

    def get_delete_url(self):
        return reverse("blog:delete_post", args=[self.id])

    def get_update_url(self):
        return reverse("blog:update_post", args=[self.id])