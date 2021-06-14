from django import forms
from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    is_public = forms.ChoiceField(
        choices=(('1', 'Public'), ('0', 'Connection Only')),
        required=False,
    )

    class Meta:
        model = Post
        fields = ['picture', 'content', 'is_public']
