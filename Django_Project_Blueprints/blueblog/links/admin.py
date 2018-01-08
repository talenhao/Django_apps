from django.contrib import admin

# Register your models here.
from links.models import Link, Comment

admin.site.register(Link)
admin.site.register(Comment)