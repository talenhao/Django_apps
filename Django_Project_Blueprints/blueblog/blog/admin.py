from django.contrib import admin


# Register your models here.
from blog.models import Blog
from blog.models import BlogPost


class BlogAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'slug')
    list_filter = ('owner',)
    search_fields = ('title',)


admin.site.register(Blog, BlogAdmin)


class BlogPostAdmin(admin.ModelAdmin):
    list_filter = ('blog', 'title', 'slug', 'body', 'is_published')
    list_display = ('title', 'slug', 'is_published')


admin.site.register(BlogPost, BlogPostAdmin)