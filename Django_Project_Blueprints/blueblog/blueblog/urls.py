"""blueblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from accounts.views import UserRegistrationView
# from django.views.generic import TemplateView

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import logout

from blog.views import NewBlogView
from blog.views import HomeView
from blog.views import UpdateBlogView
from blog.views import NewBlogPostView
from blog.views import UpdateBlogPostView
from blog.views import BlogPostDetailView
from blog.views import ShareBlogPostView
from blog.views import SharePostWithBlog
from blog.views import StopSharingPostWithBlog


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', TemplateView.as_view(template_name='accounts/base.html'), name='home'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^new-user$', UserRegistrationView.as_view(), name='user_registration'),
    url(r'^login/$', LoginView.as_view(template_name="accounts/login.html"), name='login'),
    url(r'^logout/$', logout, {"next_page": "/login/"}, name='logout'),
    url(r'^blog/new/$', NewBlogView.as_view(), name='new-blog'),
    url(r'^blog/(?P<pk>\d+)/update/$', UpdateBlogView.as_view(), name='update-blog'),
    url(r'^blog/post/new/$', NewBlogPostView.as_view(), name='new-blog-post'),
    url(r'^blog/post/(?P<pk>\d+)/update/$', UpdateBlogPostView.as_view(), name='update-blog-post'),
    url(r'^blog/post/(?P<pk>\d+)/$', BlogPostDetailView.as_view(), name='blog-post-detail'),
    url(r'^blog/post/(?P<pk>\d+)/share/$', ShareBlogPostView.as_view(), name='share_blog_post'),
    url(r'^blog/post/(?P<post_pk>\d+)/share/to/(?P<blog_pk>\d+)/$',
        SharePostWithBlog.as_view(), name='share_post_with_blog'),
    url(r'^blog/post/(?P<post_pk>\d+)/stop/share/to/(?P<blog_pk>\d+)/$',
        StopSharingPostWithBlog.as_view(), name='stop_share_post_with_blog'),
]
