from django import forms
from links.models import Comment


class CommentModelForm(forms.ModelForm):
    link_pk = forms.IntegerField(widget=forms.HiddenInput)
    comment_parent_pk = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = (
            'body',
        )
