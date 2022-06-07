from dataclasses import fields
from django import forms
from courses.models import Course
from notes.models import Note
from .models import Profile
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
import re
from django.core import validators
from .models import User


def notValidEmail(email):
    try:
        validators.validate_email(email)
    except ValidationError as e:
        return True
    else:
        False


def notValidPassword(password):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*_=+-]).{8,12}$"
    pat = re.compile(reg)
    mat = re.search(pat, password)
    if mat or len(password) >= 8:
        return False
    else:
        return True


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

        def clean(self):
            super(CustomUserCreationForm, self).clean()

            first_name = self.cleaned_data.get('first_name')
            last_name = self.cleaned_data.get('last_name')
            email = self.cleaned_data.get('email')
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')

            if len(first_name) < 3:
                self._errors['first_name'] = self.error_class([
                    'Name too short, minimum 3 characters required'])
                print('Name too short, minimum 3 characters required')
            if len(last_name) < 3:
                self._errors['last_name'] = self.error_class([
                    'Name too short, minimum 3 characters required'])
                print("'Name too short, minimum 3 characters required'")
            if notValidEmail(email):
                self._errors['email'] = self.error_class([
                    'Please enter a valid email'])

            if notValidPassword(password1):
                self._errors['password1'] = self.error_class([
                    'Password Should Contain a minimum of 8 characters and at least: one capital, one small letter, one number and one special symbol'])
            if password1 != password2:
                self.errors["password2"] = self.error_class([
                    'Passwords mismatch'
                ])
            return self.cleaned_data


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_(u'Name'), max_length=50)
    last_name = forms.CharField(label=_(u'Surname'), max_length=50)
    email = forms.CharField(label=_(u'email'), max_length=50)

    def __init__(self, *args, **kw):
        super(UserProfileForm, self).__init__(*args, **kw)
        self.fields['email'].initial = self.instance.user.email
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, *args, **kw):
        super(UserProfileForm, self).save(*args, **kw)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.save()

    class Meta:
        model = Profile
        fields = ['image', 'profile_name', 'about', 'first_name', 'last_name', 'phone',
                  'gender', 'date_of_birth',  'school', 'school_level', 'program']
