from django.shortcuts import render
from main.models import Home, About, Contact
from notes.models import Note
from courses.models import Course
from discussions.models import Post
from quizzes.models import Quiz
from users.models import User, Review
from django.http import JsonResponse
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView,	UpdateView,	DeleteView
from django.urls import reverse_lazy

# Create your views here.


class DashboardView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'back/administers/dashboard.html'

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        user = request.user
        last_activity = user.profile.last_activity
        new_messages = Contact.objects.filter(
            date__gte=last_activity).count()
        new_posts = Post.objects.filter(date__gte=last_activity).count()
        new_notes = Note.objects.filter(created__gte=last_activity).count()
        new_courses = Course.objects.filter(created__gte=last_activity).count()
        new_quizzes = Quiz.objects.filter(created__gte=last_activity).count()
        new_reviews = Review.objects.filter(date__gte=last_activity).count()
        new_users = User.objects.filter(date_joined__gte=last_activity).count()
        total_posts = Post.objects.all().count()
        total_courses = Course.objects.all().count()
        total_notes = Note.objects.all().count()
        total_quizzes = Quiz.objects.all().count()
        total_users = User.objects.all().count()
        total_reviews = Review.objects.all().count()
        print(new_messages, new_courses, new_notes, new_posts,
              new_quizzes, new_reviews, new_users, total_reviews)
        return self.render_to_response({'dashboard': True, 'site': site, 'about': about, 'user': user, 'new_users': new_users, 'new_messages': new_messages, 'new_courses': new_courses,
                                        'new_notes': new_notes, 'new_quizzes': new_quizzes, 'new_posts': new_posts, 'new_reviews': new_reviews, 'total_reviews': total_reviews, 'total_posts': total_posts,
                                        'total_courses': total_courses, 'total_notes': total_notes, 'total_quizzes': total_quizzes, 'total_users': total_users})


class NotesView(TemplateResponseMixin, View):
    template_name = 'back/administers/note_list.html'
    model = Note

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        notes = Note.objects.all()
        total_posts = Post.objects.all().count()
        total_courses = Course.objects.all().count()
        total_notes = Note.objects.all().count()
        total_quizzes = Quiz.objects.all().count()
        total_users = User.objects.all().count()
        total_reviews = Review.objects.all().count()

        return self.render_to_response({'site': site, 'about': about, 'notes': notes, 'total_reviews': total_reviews, 'total_posts': total_posts,
                                        'total_courses': total_courses, 'total_notes': total_notes, 'total_quizzes': total_quizzes, 'total_users': total_users})

    def post(self,	request, *args, **kwargs):
        pk = request.POST['note_id']
        try:
            note = get_object_or_404(
                Note, id=pk)
            if (note.verified == 0):
                Note.objects.filter(pk=pk).update(verified=1)
                return JsonResponse({"success": True, "message": "note verified!", 'text': 'Verify'})
            else:
                Note.objects.filter(pk=pk).update(verified=0)
                return JsonResponse({"success": True, "message": "note de-verified!", 'text': 'Un-Verify'})

        except:
            return JsonResponse({"success": False, "message": "Error verifying note"})


class NoteUpdateView(PermissionRequiredMixin,	UpdateView):
    model = Note
    permission_required = 'notes.change_note'
    template_name = 'front/notes/manage/form.html'
    success_url = reverse_lazy('admin_dashboard')
    fields = ['school_level', 'subject', 'title',
              'description', 'body', 'file', 'tags']
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class NoteDeleteView(PermissionRequiredMixin, LoginRequiredMixin,	DeleteView):
    model = Note
    template_name = 'front/notes/manage/delete.html'
    success_url = reverse_lazy('admin_dashboard')
    permission_required = 'notes.delete_note'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}
