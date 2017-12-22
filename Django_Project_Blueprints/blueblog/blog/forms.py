#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
"""
 @Author: 郝天飞/Talen Hao (talenhao@gmail.com)
 @Site: talenhao.github.io
 @Since: 2017/12/21 11:54 PM 
"""


from django import forms
from blog.models import Blog

from blog.models import BlogPost


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'title'
        ]


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            'title',
            'body'
        ]
