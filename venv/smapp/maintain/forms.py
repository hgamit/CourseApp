from django import forms
from .models import topic, post

from django import forms

class NewTopicForm(forms.ModelForm):
    post_message = forms.CharField(
         label='To Request New Softwares/Versions and More. Post Here',
        widget=forms.Textarea(
        attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000. Add New Software/Version Details.'
    )

    topic_software = forms.CharField(
        label='Choose from Existing Softwares',
        max_length=500,
        help_text='Start Typing Software Name. [Multiple Entries ALLOWED]'
    )

    class Meta:
        model = topic
        fields = ['topic_subject', 'topic_software','post_message']

class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['post_message', ]