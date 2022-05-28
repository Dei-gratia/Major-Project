from django import forms
from django.forms.models import inlineformset_factory
from .models import Quiz,	Question

QuestionFormSet = inlineformset_factory(Quiz,
                                        Question,
                                        fields=['question',
                                                'option1',
                                                'option2',
                                                'option3',
                                                'option4',
                                                'correct_option'],
                                        extra=5,
                                        can_delete=True)
