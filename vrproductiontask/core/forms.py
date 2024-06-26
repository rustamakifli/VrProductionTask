from django import forms
from core.models import BlogComment
from ckeditor.widgets import CKEditorWidget


class BlogCommentForm(forms.ModelForm):

    class Meta:
        model = BlogComment
        fields = (
            'comment',
        )
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Name here'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email here'
            }),
            'comment': forms.Textarea(attrs={
                'cols': 40,
                'rows': 5,
                'placeholder': 'Comment here'
            })
        }

from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'image', 'description', 'content',  'category','tags']
        # widgets = {
        #     'tags': forms.SelectMultiple(attrs={'class': ''}),
        # }
