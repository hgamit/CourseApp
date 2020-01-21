from django import forms
from .models import topic, post

from django import forms

class NewTopicForm(forms.ModelForm):
    post_message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = topic
        fields = ['topic_subject', 'post_message']

class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['post_message', ]