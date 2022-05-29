from django import forms
from django.forms.models import inlineformset_factory
from .models import DiscussionTopic,	Post

PostFormSet = inlineformset_factory(DiscussionTopic,
                                    Post,
                                    fields=['discussion_topic',
                                            'title',
                                            'post_content',
                                            'image'],
                                    extra=2,
                                    can_delete=True)
