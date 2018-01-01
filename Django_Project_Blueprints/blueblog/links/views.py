from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from links.models import Link
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

from links.forms import CommentModelForm
from links.models import Comment


class NewSubmissionView(CreateView):
    model = Link
    fields = (
        'title', 'url'
    )
    
    template_name = 'links/new_submission.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewSubmissionView, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        new_link = form.save(commit=False)
        new_link.submitted_by = self.request.user
        new_link.save()
        self.object = new_link
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        # return reverse('links-home')
        return reverse('submission-detail', kwargs={'pk': self.object.pk})


class SubmissionDetailView(DetailView):
    model = Link
    template_name = 'links/submission_detail.html'

    # 为了显示当前submission的所有comments，先获取get_context_data
    def get_context_data(self, **kwargs):
        ctx = super(SubmissionDetailView, self).get_context_data(**kwargs)
        # 当前已经存在的comments
        submission_comments = Comment.objects.filter(commented_to=self.object)
        ctx['comments'] = submission_comments
        # Display new comment from
        ctx['comment_form'] = CommentModelForm(initial={"link_pk": self.object.pk})
        return ctx


class NewCommentView(CreateView):
    form_class = CommentModelForm
    http_method_names = ('post',)
    template_name = "links/comment.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewCommentView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        parent_link = Link.objects.get(pk=form.cleaned_data['link_pk'])
        new_comment = form.save(commit=False)
        new_comment.commented_to = parent_link
        new_comment.commented_by = self.request.user
        new_comment.save()
        # 验证成功，跳转到detail页
        return HttpResponseRedirect(reverse('submission-detail', kwargs={'pk': parent_link.pk}))

    def get_initial(self):
        initial_data = super(NewCommentView, self).get_initial()
        initial_data['link_pk'] = self.request.GET['link_pk']

    def get_context_data(self, **kwargs):
        ctx = super(NewCommentView, self).get_context_data(**kwargs)
        ctx['submission'] = Link.objects.get(pk=self.request.GET['link_pk'])
        return ctx


class NewCommentReplyView(CreateView):
    form_class = CommentModelForm
    # http_method_names = ('post',)
    template_name = 'links/comment_reply.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewCommentReplyView, self).dispatch(request, *args, **kwargs)

    # before submit
    def get_context_data(self, **kwargs):
        ctx = super(NewCommentReplyView, self).get_context_data(**kwargs)
        # GET使用中括号
        parent_comment_ob = Comment.objects.get(pk=self.request.GET['parent_comment_pk'])
        ctx['parent_comment'] = parent_comment_ob
        return ctx

    def get_initial(self):
        initial_data = super(NewCommentReplyView, self).get_initial()
        link_pk = self.request.GET['link_pk']
        initial_data['link_pk'] = link_pk
        parent_comment_pk = self.request.GET['parent_comment_pk']
        initial_data['parent_comment_pk'] = parent_comment_pk
        return initial_data

    # after submit
    def form_valid(self, form):
        parent_link = Link.objects.get(pk=form.cleaned_data['link_pk'])
        parent_comment_cd = Comment.objects.get(pk=form.cleaned_data['parent_comment_pk'])
        new_comment = form.save(commit=False)
        new_comment.commented_by = self.request.user
        new_comment.commented_to = parent_link
        new_comment.in_reply_to = parent_comment_cd
        new_comment.save()
        return HttpResponseRedirect(reverse('submission-detail', kwargs={'pk': parent_link.pk}))


