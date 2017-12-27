from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Link
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse


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
        return reverse('home')
