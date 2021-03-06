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
from django.views.generic import TemplateView

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

from links.views import NewSubmissionView
from links.views import SubmissionDetailView
from links.views import NewCommentView
from links.views import NewCommentReplyView
from links.views import HomeView as LinkHomeView
from links.views import UpvoteSubmissionView
from links.views import RemovevoteSubmissionView

from data_collector.views import StatusView, AlertListView, UpdateAlertView, CreateAlertView, DeleteAlertView
from data_collector.views import RecordDataApiView
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.conf.urls import include

from django.conf.urls.static import static

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
    # for links
    # url(r'^links/$', TemplateView.as_view(template_name='links/home.html'), name='links-home'),
    url(r'^links/$', LinkHomeView.as_view(), name='links-home'),
    url(r'^new-submission/$', NewSubmissionView.as_view(), name='new-submission'),
    url(r'^submission/(?P<pk>\d+)/$', SubmissionDetailView.as_view(), name='submission-detail'),
    url(r'^new-comment/$', NewCommentView.as_view(), name='new-comment'),
    url(r'^new-comment-reply/$', NewCommentReplyView.as_view(), name='new-comment-reply'),
    # votes
    url(r'^upvote/(?P<link_pk>\d+)/$', UpvoteSubmissionView.as_view(), name='upvote-submission'),
    url(r'^upvote/(?P<link_pk>\d+)/remove/$', RemovevoteSubmissionView.as_view(), name='remove-upvote-submission'),

    # data_collector
    url(r'^data_collector/$', StatusView.as_view(), name='status'),
    url(r'^data_collector/alerts/$', AlertListView.as_view(), name='alerts_list'),
    url(r'^data_collector/new-alert/$', CreateAlertView.as_view(), name='new_alert'),
    url(r'^data_collector/(?P<pk>\d+)/update-alert/$', UpdateAlertView.as_view(), name='update_alert'),
    url(r'^data_collector/(?P<pk>\d+)/delete-alert/$', DeleteAlertView.as_view(), name='delete_alert'),
    # The csrf_exempt decorator is used because, by default, Django uses CSRF protection for POST requests.
    url(r'^record/$', csrf_exempt(RecordDataApiView.as_view()), name='record'),

    # car rental
    url(r'^car/', include('carrental.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
