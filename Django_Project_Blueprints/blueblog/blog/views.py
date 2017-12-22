from django.shortcuts import render

# Create your views here.
from blog.forms import BlogForm
from django.views.generic import CreateView
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from blog.models import Blog
from django.http.response import HttpResponseForbidden

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

from django.views.generic import UpdateView

from blog.forms import BlogPostForm

class NewBlogView(CreateView):
    form_class = BlogForm
    template_name = 'blog/blog_settings.html'
    
    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.owner = self.request.user
        blog_obj.slug = slugify(blog_obj.title)
        
        blog_obj.save()
        return HttpResponseRedirect(reverse('home'))
    
    # 多个blog检测
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if Blog.objects.filter(owner=user):
            return HttpResponseForbidden('禁止创建多个Blog')
        else:
            return super(NewBlogView, self).dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            if Blog.objects.filter(owner=self.request.user).exists():
                ctx['has_blog'] = True
                ctx['blog'] = Blog.objects.get(owner=self.request.user)
            # ctx['has_blog'] = Blog.objects.filter(owner=self.request.user).exists()
        return ctx


class UpdateBlogView(UpdateView):
    form_class = BlogForm
    template_name = 'blog/blog_settings.html'
    success_url = '/'
    model = Blog

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateBlogView, self).dispatch(request, *args, **kwargs)


class NewBlogPostView(CreateView):
    form_class = BlogPostForm
    template_name = 'blog/blog_post.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewBlogPostView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        blog_post_obj = form.save(commit=False)
        blog_post_obj.blog = Blog.objects.get(owner=self.request.user)
        blog_post_obj.slug = slugify(blog_post_obj.title)
        blog_post_obj.is_published = True
        blog_post_obj.save()
        return HttpResponseRedirect(reverse('home'))