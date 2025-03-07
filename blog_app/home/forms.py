from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=40)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','body']


class SearchForm(forms.Form):   # form for searching posts
    query = forms.CharField()