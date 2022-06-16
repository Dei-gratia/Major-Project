from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,	UpdateView,	DeleteView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.forms.models import modelform_factory
from .models import Module, Content
from .forms import ModuleFormSet
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from .models import Subject
from django.views.generic.detail import DetailView
from users.forms import CourseEnrollForm
from main.models import Home, About, SchoolLevel
from main.mixins import OwnerEditMixin, OwnerMixin
from django.db.models import Q, CharField


# Create your views here.
def search(request):
    site = Home.objects.latest('updated')
    about = About.objects.latest('updated')
    print('in search')
    if request.method == 'GET':  # this will be GET now
        # do some research what it does
        search_query = request.GET.get('search')
        print(search_query)
        # Add your models here, in any way you find best.
        search_models = [Course, Module]

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


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['school_level', 'subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin,	OwnerEditMixin):
    fields = ['school_level', 'subject', 'title', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'front/courses/manage/course/form.html'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated'),
                     'latest': Course.objects.all().order_by('-created')[:5]}


class ManageCourseListView(OwnerCourseMixin,	ListView):
    template_name = 'front/courses/manage/course/list.html'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin,	CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin,	UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin,	DeleteView):
    template_name = 'front/courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated'),
                     'latest': Course.objects.all().order_by('-created')[:5]}


class CourseModuleUpdateView(TemplateResponseMixin,	View):
    template_name = 'front/courses/manage/module/formset.html'
    course = None

    def get_formset(self,	data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self,	request,	pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request,	pk)

    def get(self,	request,	*args,	**kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course':	self.course, 'formset':	formset, 'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated')})

    def post(self,	request,	*args,	**kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course':	self.course, 'formset':	formset, 'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated')})


class ContentCreateUpdateView(TemplateResponseMixin,	View):
    module = None
    model = None
    obj = None
    template_name = 'front/courses/manage/content/form.html'

    def get_model(self,	model_name):
        if model_name in ['text',	'video',	'image',	'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self,	model,	*args,	**kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args,	**kwargs)

    def dispatch(self,	request,	module_id,	model_name,	id=None):
        self.module = get_object_or_404(
            Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super(ContentCreateUpdateView, self).dispatch(request,	module_id,	model_name,	id)

    def get(self,	request,	module_id,	model_name,	id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form':	form, 'object':	self.obj, 'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated'), 'latest': Course.objects.all().order_by('-created')[:5]})

    def post(self,	request,	module_id,	model_name,	id=None):
        form = self.get_form(self.model, instance=self.obj,
                             data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                #	new	content
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list',	self.module.id)
        return self.render_to_response({'form':	form, 'object':	self.obj, 'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated'), 'latest': Course.objects.all().order_by('-created')[:5]})


class ContentDeleteView(LoginRequiredMixin, View):
    def post(self,	request,	id):
        content = get_object_or_404(
            Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list',	module.id)


class ModuleContentListView(TemplateResponseMixin,	View):
    template_name = 'front/courses/manage/module/content_list.html'

    def get(self,	request,	module_id):
        module = get_object_or_404(
            Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module':	module, 'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated'),
                                        'latest': Course.objects.all().order_by('-created')[:5]})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, 	View):
    def post(self,	request):
        for id,	order in self.request_json.items():
            Module.objects.filter(id=id,
                                  course__owner=request.user).update(order=order)
        return self.render_json_response({'saved':	'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self,	request):
        for id,	order in self.request_json.items():
            Content.objects.filter(id=id,
                                   module__course__owner=request.user)	\
                .update(order=order)
        return self.render_json_response({'saved':	'OK'})


class CourseListView(TemplateResponseMixin,	View):
    model = Course
    template_name = 'front/courses/course/list.html'

    def get_queryset(self):
        result = super(CourseListView, self).get_queryset()
        query = self.request.GET.get('search')
        print(query)
        if query:
            postresult = Course.objects.filter(
                title__contains=query, oeverview__contains=query)
            result = postresult
        else:
            result = None
        print(result)
        return result

    def get(self,	request, order='-created', subject=None, school_level=None):
        school_levels = SchoolLevel.objects.annotate(
            total_courses=Count('courses'))
        subjects = Subject.objects.annotate(total_courses=Count('courses'))
        courses = Course.objects.annotate(
            total_modules=Count('modules')).order_by(order)

        if school_level:
            school_level = get_object_or_404(SchoolLevel, slug=school_level)
            courses = courses.filter(school_level=school_level).order_by(order)

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject).order_by(order)

        return self.render_to_response({
            'school_levels': school_levels,
            'school_level': school_level,
            'subjects':	subjects,
            'subject':	subject,
            'courses':	courses,
            'order': order,
            'site': Home.objects.latest('updated'),
            'about': About.objects.latest('updated'),
            'latest': Course.objects.all().order_by('-created')[:5]})


class CourseDetailView(DetailView):
    model = Course
    template_name = 'front/courses/course/detail.html'

    def get_context_data(self,	**kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object})

        if self.request.user.is_authenticated:
            user_review = self.object.reviews.filter(user=self.request.user)
            user_review = user_review[0]
        else:
            user_review = False

        context['site'] = Home.objects.latest('updated')
        context['about'] = About.objects.latest('updated')
        context['latest'] = Course.objects.all().order_by('-created')[:5]
        context['user_review'] = user_review
        students = kwargs['object'].students.all()
        if self.request.user in students:
            context['student'] = self.request.user

        return context
