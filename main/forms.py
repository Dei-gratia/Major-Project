from django.forms import ModelForm, EmailField, EmailInput, Form
from .models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class SubscriberForm(Form):
    email = EmailField(label='Your email',
                             max_length=100,
                             widget=EmailInput(attrs={'class': 'form-control'}))
