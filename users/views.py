import email
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from requests import request
from main.models import Home, About, SchoolLevel, Specialisation, Subject
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,	login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import SchoolLevel, Subject, Specialisation
from users.models import User, Profile
from .forms import CourseEnrollForm, UserProfileForm
from django.views.generic.list import ListView
from courses.models import Course
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from main.models import Home, About
from users.models import User, Review
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
import time


# Create your views here.
genders = ["M", 'F']


def login_view(request):
    login_form, registration_form = False, False
    if request.method == "POST":
        if "first_name" not in request.POST:  # some condition to distinguish between login and registration form
            email = request.POST['email']
            password = request.POST['password']
            print(email, password)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                print("logged in", user.profile)
                return JsonResponse({"success": True, "message": "Successfully loggedin"})
            else:
                print("not logged in", user)
                return JsonResponse({"success": False, "message": True, "message": "Invalid Login details"})
        else:
            registration_form = CustomUserCreationForm(request.POST)
            print(registration_form)

            if registration_form.is_valid():
                # register
                print(registration_form)
                print("is valid")
                user = registration_form.save()
                login(request, user)
                print("logged in", user)
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
        print(user_email)
        return JsonResponse({"success": True, "message": True, "message": "Password reset link sent, please check you email"})


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
        print(course)
        user_review = course.reviews.filter(user=request.user)
        if len(user_review) > 0:
            user_review = user_review[0]
        else:
            user_review = False
        print(user_review)

        if comment == "" and rating == "":

            return JsonResponse({"success": False, "message": "Please provide a rating or comment"})
        if user_review:
            course_total_ratings = float(course.total_ratings) -\
                float(user_review[0].rate_value) + float(rating)
            course_num_ratings = int(course.num_ratings)
            # Review.objects.filter(user=user_review.user).update(rate_value=rating, comment=comment)
            user_review.update(rate_value=rating, comment=comment)
            print(user_review[0])
            print(course_num_ratings, course_total_ratings)
        else:
            review = Review(content_object=course, user=request.user,
                            rate_value=rating, comment=comment)
            review.save()
            course_num_ratings = int(course.num_ratings) + 1
            course_total_ratings = int(course.total_ratings) + int(rating)

        print(course_num_ratings, course_total_ratings)
        Course.objects.filter(pk=pk).update(total_ratings=course_total_ratings,
                                            num_ratings=course_num_ratings)

        return JsonResponse({"success": True, "message": "Successfully rated"})
