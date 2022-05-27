from django.shortcuts import render
from main.models import Home, About, SchoolLevel, Specialisation
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,	login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from courses.models import Course
from django.views.generic.detail import DetailView


# Create your views here.
genders = ["Male", 'Female']


def user_profile(request):
    site = Home.objects.latest('updated')
    about = About.objects.latest('updated')
    school_levels = SchoolLevel.objects.all()
    specializations = Specialisation.objects.all()

    current_user = request.user

    context = {
        'site': site,
        'about': about,
        'user': current_user,
        'school_levels': school_levels,
        'specializations': specializations,
        'genders': genders,

    }
    return render(request, 'front/users/user_profile.html', context)


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
