from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Link(models.Model):
    title = models.CharField(max_length=150)
    url = models.URLField()
    submitted_by = models.ForeignKey(User)
    up_votes = models.ManyToManyField(User, related_name='votes')
    submitted_on = models.DateTimeField(auto_now_add=True, editable=False)
