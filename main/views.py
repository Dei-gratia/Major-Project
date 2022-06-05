from django.shortcuts import render
from courses.models import Course
from main.models import Contact, Home, About
from .forms import ContactForm
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.http import JsonResponse
from quizzes.models import Quiz
from notes.models import Note
from discussions.models import Post
import random

# Create your views here.


def home(request):
    site = Home.objects.latest('updated')
    about = About.objects.latest('updated')
    latest_courses = Course.objects.all().order_by('-created')[:5]
    latest_notes = Note.objects.all().order_by('-created')[:5]
    latest_quizzes = Quiz.objects.all().order_by('-created')[:5]
    latest_posts = Post.objects.all().order_by('-date')[:5]

    valid_notes_id_list = Note.objects.filter().values_list('id', flat=True)
    random_notes_id_list = random.sample(
        list(valid_notes_id_list), min(len(valid_notes_id_list), 4))
    notes = Note.objects.filter(id__in=random_notes_id_list)

    valid_course_id_list = Course.objects.filter().values_list('id', flat=True)
    random_course_id_list = random.sample(
        list(valid_course_id_list), min(len(valid_course_id_list), 4))
    courses = Course.objects.filter(id__in=random_course_id_list)

    valid_quizzes_id_list = Quiz.objects.filter().values_list('id', flat=True)
    random_quizzes_id_list = random.sample(
        list(valid_quizzes_id_list), min(len(valid_quizzes_id_list), 4))
    quizzes = Quiz.objects.filter(id__in=random_quizzes_id_list)

    valid_posts_id_list = Post.objects.filter().values_list('id', flat=True)
    random_posts_id_list = random.sample(
        list(valid_posts_id_list), min(len(valid_posts_id_list), 4))
    posts = Post.objects.filter(id__in=random_posts_id_list)

    context = {
        'site': site,
        'about': about,
        'notes': notes,
        'courses': courses,
        'posts': posts,
        'quizzes': quizzes,
        'latest_courses': latest_courses,
        'latest_quizzes': latest_quizzes,
        'latest_notes': latest_notes,
        'latest_posts': latest_posts,
    }

    return render(request, 'front/main/index.html', context)


class AboutView(TemplateResponseMixin, View):
    template_name = 'front/main/about.html'

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        return self.render_to_response({'site': site, 'about': about})


class ContactView(TemplateResponseMixin, View):
    template_name = 'front/main/contact.html'
    model = Contact

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        form = ContactForm()
        return self.render_to_response({'site': site, 'about': about, 'form': form})

    def post(self,	request,	*args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            # form.save()
            contact_email = form.cleaned_data['email']
            email_subject = f'Major project new contact: {form.cleaned_data["name"]}, {form.cleaned_data["email"]}'
            email_message = form.cleaned_data['message']
            print(contact_email, email_subject, email_message)

        return JsonResponse({"success": True, "message": "Thank you for getting in touch, our team will get back to you"})
