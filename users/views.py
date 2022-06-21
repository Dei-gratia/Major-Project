import email
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from requests import request
from discussions.models import Post
from main.models import Home, About, SchoolLevel, Specialisation, Subject
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,	login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import SchoolLevel, Subject, Specialisation
from notes.models import Note
from quizzes.models import Quiz
from django.db.models import Count
from users.models import User, Profile
from .forms import CourseEnrollForm, UserProfileForm
from django.views.generic.list import ListView
from courses.models import Course
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from main.models import Home, About, Contact
from users.models import User, Review
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib import messages
import re


# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# Create your views here.
genders = ["M", 'F']


def login_view(request):
    login_form, registration_form = False, False
    if request.method == "POST":
        if "first_name" not in request.POST:  # some condition to distinguish between login and registration form
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"success": True, "message": "Successfully loggedin"})
            else:
                return JsonResponse({"success": False, "message": True, "message": "Invalid Login details"})
        else:
            registration_form = CustomUserCreationForm(request.POST)

            if registration_form.is_valid():
                # register
                user = registration_form.save()
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                return JsonResponse({"success": True, "message": "Successfully loggedin"})
            else:
                print("is not valid")

    obj = {
        'login_form': login_form if login_form else CustomAuthenticationForm(),
        'registration_form': registration_form if registration_form else CustomUserCreationForm(),
    }
    return render(request, 'front/users/authentication.html', obj)


def logout_view(request):
    logout(request)
    return redirect("login")


def password_reset(request):
    if request.method == "POST":
        user_email = request.POST['user_email']
        if(re.fullmatch(regex, user_email)):
            associated_users = User.objects.filter(Q(email=user_email))
            if associated_users.exists():
                for user in associated_users:
                    subject = "E-Learn | Password Reset Requested"
                    email_template_name = "front/users/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'E-Learn',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.CONTACT_EMAIL,
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(
                        request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("home")
            else:
                messages.error(request, "No such user with given email")
                return redirect('login')
        else:
            messages.error(request, "Invalid email address")
            return redirect('login')


def email_reset(request):
    if request.method == "POST":
        user_email = request.POST['email']
        print(user_email)
        return JsonResponse({"success": False, "message": True, "message": "Email"})


class UserProfile(UpdateView):
    model = Profile
    context_object_name = 'user'
    queryset = Profile.objects.all()
    form_class = UserProfileForm
    template_name = 'front/users/user_profile.html'

    def get_success_url(self):
        return reverse('user_profile', kwargs={'pk': self.get_object().user.id})

    def get_object(self, **kwargs):
        pk = self.kwargs.get("pk")
        if pk is None:
            raise Http404
        return get_object_or_404(Profile, user__pk__iexact=pk)

    def get_context_data(self,	**kwargs):
        context = super(UserProfile,
                        self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['user_form'] = UserProfileForm(
            instance=self.request.user.profile)
        context['site'] = Home.objects.latest('updated')
        context['about'] = About.objects.latest('updated')
        context['school_levels'] = SchoolLevel.objects.all()
        context['specializations'] = SchoolLevel.objects.all()
        context['genders'] = genders

        return context


class StudentEnrollCourseView(LoginRequiredMixin,	FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        print(self.course, type(self.course))
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin,	ListView):
    model = Course
    template_name = 'front/users/course/list.html'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self,	**kwargs):
        context = super(StudentCourseListView, self).get_context_data(**kwargs)
        context['site'] = Home.objects.latest('updated')
        context['about'] = About.objects.latest('updated')
        return context


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'front/users/course/detail.html'

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self,	**kwargs):
        context = super(StudentCourseDetailView,
                        self).get_context_data(**kwargs)
        #	get	course	object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            #	get	current	module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id'])
        else:
            #	get	first	module
            context['module'] = course.modules.all()[0]
        context['site'] = Home.objects.latest('updated')
        context['about'] = About.objects.latest('updated')
        return context

    def post(self, request, *args, pk, **kwargs):
        userprofile = request.user.profile
        comment = request.POST['comment']
        rating = request.POST['input-1']
        course = get_object_or_404(
            Course, id=pk, owner=request.user)
        user_review = course.reviews.filter(user=request.user)
        if len(user_review) > 0:
            user_review = user_review[0]
        else:
            user_review = False

        if comment == "" and rating == "":

            return JsonResponse({"success": False, "message": "Please provide a rating or comment"})
        if user_review:
            course_total_ratings = float(course.total_ratings) -\
                float(user_review[0].rate_value) + float(rating)
            course_num_ratings = int(course.num_ratings)
            # Review.objects.filter(user=user_review.user).update(rate_value=rating, comment=comment)
            user_review.update(rate_value=rating, comment=comment)
        else:
            review = Review(content_object=course, user=request.user,
                            rate_value=rating, comment=comment)
            review.save()
            course_num_ratings = int(course.num_ratings) + 1
            course_total_ratings = int(course.total_ratings) + int(rating)

        Course.objects.filter(pk=pk).update(total_ratings=course_total_ratings,
                                            num_ratings=course_num_ratings)

        return JsonResponse({"success": True, "message": "Successfully rated"})


class DashboardView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'front/users/dashboard.html'

    def get(self,	request, pk):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        user = get_object_or_404(User, pk__iexact=pk)
        posts = Post.objects.filter(owner=user)
        notes = Note.objects.filter(owner=user)
        courses = Course.objects.filter(owner=user)
        quizzes = Quiz.objects.filter(owner=user)
        reviews = Review.objects.filter(user=user)

        return self.render_to_response({'site': site, 'about': about, 'user': user,  'courses': courses,
                                        'notes': notes, 'quizzes': quizzes, 'posts': posts, 'reviews': reviews, })
