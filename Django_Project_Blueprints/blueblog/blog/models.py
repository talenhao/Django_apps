from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Blog(models.Model):
    owner = models.ForeignKey(User, editable=False)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, editable=False)

    def __str__(self):
        return self.title
    

class BlogPost(models.Model):
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, editable=False)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    shared_to = models.ManyToManyField(Blog, related_name='shared_posts')
