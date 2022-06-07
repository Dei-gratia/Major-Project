from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count
from requests import request
from .models import Note
from users.models import Review, Profile
from main.models import Subject, SchoolLevel, Home, About
from django.views.generic.detail import DetailView
from main.mixins import OwnerEditMixin, OwnerMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.views.generic.edit import CreateView,	UpdateView,	DeleteView

# Create your views here.


class NoteListView(TemplateResponseMixin,	View):
    model = Note
    template_name = 'front/notes/note/list.html'

    def get(self,	request,	order='-created', subject=None, school_level=None):
        subjects = Subject.objects.annotate(total_notes=Count('notes'))
        school_levels = SchoolLevel.objects.annotate(
            total_notes=Count('notes'))
        notes = Note.objects.annotate(total_reviews=Count('reviews'))
        latest = Note.objects.all().order_by('-created')[:5]

        if school_level:
            school_level = get_object_or_404(SchoolLevel, slug=school_level)
            notes = notes.filter(school_level=school_level).order_by(order)

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            notes = notes.filter(subject=subject).order_by(order)

        return self.render_to_response({
            'order': order,
            'school_levels': school_levels,
            'school_level': school_level, 'subjects':	subjects,
            'subject':	subject,
            'notes':	notes,
            'site': Home.objects.latest('updated'),
            'about': About.objects.latest('updated'),
            'latest': latest,
        })


def save_note(request, note_id):
    note = Note.objects.get(id=note_id)
    if request.user in note.students.all():
        note.students.remove(request.user)
        print(note.students.all())
        return JsonResponse({"success": True, "message": "Note saved"})
    else:
        note.students.add(request.user)
        return JsonResponse({"success": True, "message": "Note saved"})


class NoteDetailView(DetailView):
    model = Note
    template_name = 'front/notes/note/detail.html'

    def get_context_data(self,	**kwargs):
        context = super(NoteDetailView, self).get_context_data(**kwargs)
        context['site'] = Home.objects.latest('updated')
        context['about'] = About.objects.latest('updated')
        context['latest'] = Note.objects.all().order_by('-created')[:5]
        saved = False
        if self.request.user.is_authenticated:
            user_review = self.object.reviews.filter(user=self.request.user)
            if len(user_review) > 0:
                user_review = user_review[0]
            else:
                user_review = False
                context['user_review'] = user_review
                print(user_review)
            if self.request.user in self.object.students.all():
                saved = True
                context['saved'] = saved
        return context

    def post(self, request, *args, pk, **kwargs):
        userprofile = request.user.profile
        print(args, kwargs, pk)
        print(userprofile, '\n'*5)
        comment = request.POST['comment']
        rating = request.POST['input-1']
        print(rating, comment, userprofile)
        note = get_object_or_404(
            Note, id=pk, owner=request.user)
        print(note)
        user_review = note.reviews.filter(user=request.user)
        print(user_review)

        if comment == "" and rating == "":

            return JsonResponse({"success": False, "message": "Please provide a rating or comment"})
        if user_review:
            note_total_ratings = int(note.total_ratings) -\
                int(user_review[0].rate_value) + int(rating)
            note_num_ratings = int(note.num_ratings)
            # Review.objects.filter(user=user_review.user).update(rate_value=rating, comment=comment)
            user_review.update(rate_value=rating, comment=comment)
            print(user_review[0])
            print(note_num_ratings, note_total_ratings)
        else:
            review = Review(content_object=note, user=request.user,
                            rate_value=rating, comment=comment)
            review.save()
            note_num_ratings = int(note.num_ratings) + 1
            note_total_ratings = int(note.total_ratings) + int(rating)

        print(note_num_ratings, note_total_ratings)
        Note.objects.filter(pk=pk).update(total_ratings=note_total_ratings,
                                          num_ratings=note_num_ratings)

        return JsonResponse({"success": True, "message": "Successfully rated"})


class OwnerNoteMixin(OwnerMixin, LoginRequiredMixin):
    model = Note
    fields = ['school_level', 'subject',
              'title', 'description', 'file', 'tags']
    success_url = reverse_lazy('manage_note_list')


class OwnerNoteEditMixin(OwnerNoteMixin,	OwnerEditMixin):
    fields = ['school_level', 'subject', 'title',
              'description', 'body', 'file', 'tags']
    success_url = reverse_lazy('manage_note_list')
    template_name = 'front/notes/manage/form.html'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class ManageNoteListView(OwnerNoteMixin,	ListView):
    template_name = 'front/notes/manage/list.html'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class NoteCreateView(PermissionRequiredMixin, OwnerNoteEditMixin,	CreateView):
    permission_required = 'notes.add_note'


class NoteUpdateView(PermissionRequiredMixin, OwnerNoteEditMixin,	UpdateView):
    permission_required = 'notes.change_note'


class NoteDeleteView(PermissionRequiredMixin, OwnerNoteMixin,	DeleteView):
    template_name = 'front/notes/manage/delete.html'
    success_url = reverse_lazy('manage_note_list')
    permission_required = 'notes.delete_note'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}
