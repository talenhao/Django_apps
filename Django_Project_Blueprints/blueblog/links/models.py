from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Link(models.Model):
    title = models.CharField(max_length=150)
    url = models.URLField()
    submitted_by = models.ForeignKey(User)
    up_votes = models.ManyToManyField(User, related_name='votes')
    submitted_on = models.DateTimeField(auto_now_add=True, editable=False)


class Comment(models.Model):
    body = models.TextField()
    commented_to = models.ForeignKey(Link)
    in_reply_to = models.ForeignKey('self', null=True)
    commented_by = models.ForeignKey(User)
    commented_on = models.DateTimeField(auto_now_add=True, editable=False)
