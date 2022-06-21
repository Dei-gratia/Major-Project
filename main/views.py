from django.shortcuts import render, redirect
from courses.models import Course
from main.models import Contact, Home, About, Subscriber
from .forms import ContactForm, SubscriberForm
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.http import JsonResponse
from quizzes.models import Quiz
from notes.models import Note
from discussions.models import DiscussionTopic, Post
import random
from django.db.models import Q, CharField
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
import re


# Create your views here.
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


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
        'latest': latest_courses,
        'latest_courses': latest_courses,
        'latest_quizzes': latest_quizzes,
        'latest_notes': latest_notes,
        'latest_posts': latest_posts,
    }

    return render(request, 'front/main/index.html', context)


def search_all(request):
    site = Home.objects.latest('updated')
    about = About.objects.latest('updated')
    if request.method == 'GET':  # this will be GET now
        # do some research what it does
        search_query = request.GET.get('search')
        # Add your models here, in any way you find best.
        search_models = [Course, Note, Quiz, DiscussionTopic, Post]

        search_results = []
        for model in search_models:
            fields = [x for x in model._meta.fields if isinstance(
                x, CharField)]
            search_queries = [
                Q(**{x.name + "__contains": search_query}) for x in fields]
            q_object = Q()
            for query in search_queries:
                q_object = q_object | query

            results = model.objects.filter(q_object)
            results.model_name = results.model.__name__
            search_results.append(results)
        return render(request, "front/main/search.html", {"site": site, "about": about, "query": search_query, "results": search_results})
    else:
        return render(request, "front/main/search.html", {"site": site, "about": about, "query": search_query})


def search(request, models_list):
    site = Home.objects.latest('updated')
    about = About.objects.latest('updated')
    if request.method == 'GET':  # this will be GET now
        # do some research what it does
        search_query = request.GET.get('search')
    return render(request, "front/main/search.html", {"site": site, "about": about, "query": search_query})


def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)


@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email)
        if(re.fullmatch(regex, email)):
            subscriber = Subscriber.objects.filter(email=email)
            if subscriber.count() < 1:
                sub = Subscriber(email=email, conf_num=random_digits())
                sub.save()
                subject = "E-Learn | Subscription Confirmation"
                html_content = 'Hello \nThank you for signing up for my email newsletter! \
					Please complete the process by \
					<a href="{}?email={}&conf_num={} "> clicking here to \
						confirm your registration</a>.'.format(request.build_absolute_uri('/subscribe/confirm/'),
                                             sub.email,
                                             sub.conf_num)

                try:
                    print(html_content)
                    send_mail(subject, html_content, settings.CONTACT_EMAIL,
                              [sub.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(
                    request, 'Thank you for subscribing. Please check your inbox for confirmation email to complete the process! ')
                return redirect("home")
            else:
                messages.success(request, "Email address already subscribed")
                return redirect('home')
        else:
            messages.error(request, "Invalid email address")
            return redirect('home')
    else:
        return redirect('home')


def subscribe_confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    print(sub)
    print(
        f'saved number is {sub.conf_num} getted number is {request.GET["conf_num"]}')
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        messages.success(
            request, " Thank you for confirming your subscription")
        return redirect('home')
    else:
        messages.error(request, "Invalid email link. Action Denied")
        return redirect('home')


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
            form.save()
            contact_email = form.cleaned_data['email']
            contact_name = form.cleaned_data["name"]
            email_subject = f'E-Lean contact: {form.cleaned_data["name"]}, {form.cleaned_data["email"]}'
            email_message = f"Name: {contact_name}\nEmail: {contact_email}\n \n{form.cleaned_data['message']}"
            print(contact_email, email_subject, email_message)
            send_mail(email_subject, email_message,
                      settings.CONTACT_EMAIL, settings.ADMIN_EMAILS)
            return JsonResponse({"success": True, "message": "Thank you for getting in touch, our team will get back to you as soon as possible"})

        return JsonResponse({"success": False, "message": "Error sending message, Please try again"})
