from django.shortcuts import render
from main.models import Home, About, Contact
from notes.models import Note
from courses.models import Course
from discussions.models import DiscussionTopic, Post, Replie
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
        total_contacts = Contact.objects.all().count()
        print(new_messages, new_courses, new_notes, new_posts,
              new_quizzes, new_reviews, new_users, total_reviews)
        return self.render_to_response({'dashboard': True, 'site': site, 'about': about, 'user': user, 'new_users': new_users, 'new_messages': new_messages, 'new_courses': new_courses,
                                        'new_notes': new_notes, 'new_quizzes': new_quizzes, 'new_posts': new_posts, 'new_reviews': new_reviews, 'total_reviews': total_reviews, 'total_posts': total_posts,
                                        'total_courses': total_courses, 'total_notes': total_notes, 'total_quizzes': total_quizzes, 'total_users': total_users, 'total_contacts': total_contacts})


class UsersView(TemplateResponseMixin, LoginRequiredMixin, View):
    template_name = 'back/administers/users_list.html'
    model = User

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        users = User.objects.all()
        total_posts = Post.objects.all().count()
        total_courses = Course.objects.all().count()
        total_notes = Note.objects.all().count()
        total_quizzes = Quiz.objects.all().count()
        total_users = User.objects.all().count()
        total_reviews = Review.objects.all().count()
        total_contacts = Contact.objects.all().count()

        return self.render_to_response({'site': site, 'about': about, 'users': users, 'total_reviews': total_reviews, 'total_posts': total_posts,
                                        'total_courses': total_courses, 'total_notes': total_notes, 'total_quizzes': total_quizzes, 'total_users': total_users, 'total_contacts': total_contacts})

    def post(self,	request, *args, **kwargs):
        pk = request.POST['user_id']
        try:
            user = get_object_or_404(
                User, id=pk)
            if (user.is_active == False):
                User.objects.filter(pk=pk).update(is_active=True)
                return JsonResponse({"success": True, "message": "user activated!"})
            else:
                User.objects.filter(pk=pk).update(is_active=False)
                return JsonResponse({"success": True, "message": "user de-activated!"})

        except:
            return JsonResponse({"success": False, "message": "Error verifying user"})


class UserCreateView(PermissionRequiredMixin, LoginRequiredMixin,	CreateView):
    model = User
    permission_required = 'users.add_user'
    template_name = 'back/users/manage/form.html'
    success_url = reverse_lazy('back_user_list')
    fields = ['email', 'first_name', 'last_name',
              'is_staff', 'is_active']
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class UserUpdateView(PermissionRequiredMixin, LoginRequiredMixin,	UpdateView):
    model = User
    permission_required = 'users.change_user'
    template_name = 'back/users/manage/form.html'
    success_url = reverse_lazy('back_users_list')
    fields = ['email', 'first_name', 'last_name',
              'is_staff', 'is_active', ]
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class UserDeleteView(PermissionRequiredMixin, LoginRequiredMixin,	DeleteView):
    model = User
    template_name = 'back/users/manage/delete.html'
    success_url = reverse_lazy('back_users_list')
    permission_required = 'users.delete_user'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class CoursesView(TemplateResponseMixin, LoginRequiredMixin, View):
    template_name = 'back/administers/course_list.html'
    model = Course

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        courses = Course.objects.all()
        total_posts = Post.objects.all().count()
        total_courses = Course.objects.all().count()
        total_notes = Note.objects.all().count()
        total_quizzes = Quiz.objects.all().count()
        total_users = User.objects.all().count()
        total_reviews = Review.objects.all().count()
        total_contacts = Contact.objects.all().count()

        return self.render_to_response({'site': site, 'about': about, 'courses': courses, 'total_reviews': total_reviews, 'total_posts': total_posts,
                                        'total_courses': total_courses, 'total_notes': total_notes, 'total_quizzes': total_quizzes, 'total_users': total_users, 'total_contacts': total_contacts})

    def post(self,	request, *args, **kwargs):
        pk = request.POST['course_id']
        try:
            course = get_object_or_404(
                Course, id=pk)
            if (course.verified == 0):
                Course.objects.filter(pk=pk).update(verified=1)
                return JsonResponse({"success": True, "message": "course verified!"})
            else:
                Course.objects.filter(pk=pk).update(verified=0)
                return JsonResponse({"success": True, "message": "course de-verified!"})

        except:
            return JsonResponse({"success": False, "message": "Error verifying course"})


class CourseUpdateView(PermissionRequiredMixin, LoginRequiredMixin,	UpdateView):
    model = Course
    permission_required = 'courses.change_course'
    template_name = 'front/courses/manage/course/form.html'
    success_url = reverse_lazy('back_course_list')
    fields = ['school_level', 'subject', 'title',
              'overview', 'tags', 'cover_image']
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class CourseDeleteView(PermissionRequiredMixin, LoginRequiredMixin,	DeleteView):
    model = Course
    template_name = 'front/courses/manage/course/delete.html'
    success_url = reverse_lazy('back_course_list')
    permission_required = 'courses.delete_course'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class NotesView(TemplateResponseMixin, LoginRequiredMixin, View):
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
        total_contacts = Contact.objects.all().count()

        return self.render_to_response({'site': site, 'about': about, 'notes': notes, 'total_reviews': total_reviews, 'total_posts': total_posts,
                                        'total_courses': total_courses, 'total_notes': total_notes, 'total_quizzes': total_quizzes, 'total_users': total_users, 'total_contacts': total_contacts})

    def post(self,	request, *args, **kwargs):
        pk = request.POST['note_id']
        try:
            note = get_object_or_404(
                Note, id=pk)
            if (note.verified == 0):
                Note.objects.filter(pk=pk).update(verified=1)
                return JsonResponse({"success": True, "message": "note verified!"})
            else:
                Note.objects.filter(pk=pk).update(verified=0)
                return JsonResponse({"success": True, "message": "note de-verified!"})

        except:
            return JsonResponse({"success": False, "message": "Error verifying note"})


class NoteUpdateView(PermissionRequiredMixin, LoginRequiredMixin,	UpdateView):
    model = Note
    permission_required = 'notes.change_note'
    template_name = 'front/notes/manage/form.html'
    success_url = reverse_lazy('back_note_list')
    fields = ['school_level', 'subject', 'title',
              'description', 'body', 'file', 'tags']
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class NoteDeleteView(PermissionRequiredMixin, LoginRequiredMixin,	DeleteView):
    model = Note
    template_name = 'front/notes/manage/delete.html'
    success_url = reverse_lazy('back_note_list')
    permission_required = 'notes.delete_note'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class QuizzesView(TemplateResponseMixin, View):
    template_name = 'back/administers/quiz_list.html'
    model = Quiz

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        quizzes = Quiz.objects.all()
        total_posts = Post.objects.all().count()
        total_courses = Course.objects.all().count()
        total_notes = Note.objects.all().count()
        total_quizzes = Quiz.objects.all().count()
        total_users = User.objects.all().count()
        total_reviews = Review.objects.all().count()
        total_contacts = Contact.objects.all().count()

        return self.render_to_response({'site': site, 'about': about, 'quizzes': quizzes, 'total_reviews': total_reviews, 'total_posts': total_posts,
                                        'total_courses': total_courses, 'total_notes': total_notes, 'total_quizzes': total_quizzes, 'total_users': total_users, 'total_contacts': total_contacts})

    def post(self,	request, *args, **kwargs):
        pk = request.POST['quiz_id']
        try:
            quiz = get_object_or_404(
                Quiz, id=pk)
            if (quiz.verified == 0):
                Quiz.objects.filter(pk=pk).update(verified=1)
                return JsonResponse({"success": True, "message": "quiz verified!"})
            else:
                Quiz.objects.filter(pk=pk).update(verified=0)
                return JsonResponse({"success": True, "message": "quiz de-verified!"})

        except:
            return JsonResponse({"success": False, "message": "Error verifying quiz"})


class QuizUpdateView(PermissionRequiredMixin, LoginRequiredMixin,	UpdateView):
    model = Quiz
    permission_required = 'quizzes.change_quiz'
    template_name = 'front/quizzes/manage/quiz/form.html'
    success_url = reverse_lazy('back_quiz_list')
    fields = ['school_level', 'subject', 'title',
              'description', 'tags']
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class QuizDeleteView(PermissionRequiredMixin, LoginRequiredMixin,	DeleteView):
    model = Quiz
    template_name = 'front/quizzes/manage/quiz/delete.html'
    success_url = reverse_lazy('back_quiz_list')
    permission_required = 'quizzes.delete_quiz'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class DiscussionTopicView(TemplateResponseMixin, View):
    template_name = 'back/administers/discussion_topic_list.html'
    model = DiscussionTopic

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        topics = DiscussionTopic.objects.all()
        total_posts = Post.objects.all().count()
        total_courses = Course.objects.all().count()
        total_notes = Note.objects.all().count()
        total_quizzes = Quiz.objects.all().count()
        total_users = User.objects.all().count()
        total_reviews = Review.objects.all().count()
        total_contacts = Contact.objects.all().count()

        return self.render_to_response({'site': site, 'about': about, 'topics': topics, 'total_reviews': total_reviews, 'total_posts': total_posts,
                                        'total_courses': total_courses, 'total_notes': total_notes, 'total_quizzes': total_quizzes, 'total_users': total_users, 'total_contacts': total_contacts})

    def post(self,	request, *args, **kwargs):
        pk = request.POST['topic_id']
        try:
            quiz = get_object_or_404(
                DiscussionTopic, id=pk)
            if (quiz.verified == 0):
                DiscussionTopic.objects.filter(pk=pk).update(verified=1)
                return JsonResponse({"success": True, "message": "discussion topic verified!"})
            else:
                DiscussionTopic.objects.filter(pk=pk).update(verified=0)
                return JsonResponse({"success": True, "message": "discussion topic de-verified!"})

        except:
            return JsonResponse({"success": False, "message": "Error verifying discussion topic"})


class DiscussionTopicUpdateView(PermissionRequiredMixin, LoginRequiredMixin,	UpdateView):
    model = DiscussionTopic
    permission_required = 'discussions.change_discussion'
    template_name = 'front/discussions/manage/topic/form.html'
    success_url = reverse_lazy('back_topic_list')
    fields = ['school_level', 'subject', 'title', 'description',
              'cover_img', ]
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class DiscussionTopicDeleteView(PermissionRequiredMixin, LoginRequiredMixin,	DeleteView):
    model = DiscussionTopic
    template_name = 'front/discussions/manage/topic/delete.html'
    success_url = reverse_lazy('back_topic_list')
    permission_required = 'discussions.delete_discussion'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class PostsView(TemplateResponseMixin, View):
    template_name = 'back/administers/posts_list.html'
    model = Post

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        posts = Post.objects.all()
        total_posts = Post.objects.all().count()
        total_courses = Course.objects.all().count()
        total_notes = Note.objects.all().count()
        total_quizzes = Quiz.objects.all().count()
        total_users = User.objects.all().count()
        total_reviews = Review.objects.all().count()
        total_contacts = Contact.objects.all().count()

        return self.render_to_response({'site': site, 'about': about, 'posts': posts, 'total_reviews': total_reviews, 'total_posts': total_posts,
                                        'total_courses': total_courses, 'total_notes': total_notes, 'total_quizzes': total_quizzes, 'total_users': total_users, 'total_contacts': total_contacts})

    def post(self,	request, *args, **kwargs):
        pk = request.POST['post_id']
        try:
            post = get_object_or_404(
                Post, id=pk)
            if (post.verified == 0):
                Post.objects.filter(pk=pk).update(verified=1)
                return JsonResponse({"success": True, "message": "post verified!"})
            else:
                Post.objects.filter(pk=pk).update(verified=0)
                return JsonResponse({"success": True, "message": "post de-verified!"})

        except:
            return JsonResponse({"success": False, "message": "Error verifying note"})


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin,	CreateView):
    model = Post
    permission_required = 'posts.add_post'
    template_name = 'front/discussions/manage/post/form.html'
    success_url = reverse_lazy('back_post_list')
    fields = ['title', 'post_content', 'discussion_topic',
              'image']
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin,	UpdateView):
    model = Post
    permission_required = 'posts.change_note'
    template_name = 'front/discussions/manage/post/form.html'
    success_url = reverse_lazy('back_post_list')
    fields = ['title', 'post_content', 'discussion_topic',
              'image']
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin,	DeleteView):
    model = Post
    template_name = 'front/discussions/manage/post/delete.html'
    success_url = reverse_lazy('back_post_list')
    permission_required = 'posts.delete_post'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class ReplieView(TemplateResponseMixin, View):
    template_name = 'back/administers/replies_list.html'
    model = Replie

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        replies = Replie.objects.all()
        total_posts = Replie.objects.all().count()
        total_courses = Course.objects.all().count()
        total_notes = Note.objects.all().count()
        total_quizzes = Quiz.objects.all().count()
        total_users = User.objects.all().count()
        total_reviews = Review.objects.all().count()
        total_contacts = Contact.objects.all().count()
        print(replies)

        return self.render_to_response({'site': site, 'about': about, 'replies': replies, 'total_reviews': total_reviews, 'total_posts': total_posts,
                                        'total_courses': total_courses, 'total_notes': total_notes, 'total_quizzes': total_quizzes, 'total_users': total_users, 'total_contacts': total_contacts})

    def post(self,	request, *args, **kwargs):
        pk = request.POST['replie_id']
        try:
            replie = get_object_or_404(
                Replie, id=pk)
            if (replie.verified == 0):
                Replie.objects.filter(pk=pk).update(verified=1)
                return JsonResponse({"success": True, "message": "reply verified!"})
            else:
                Replie.objects.filter(pk=pk).update(verified=0)
                return JsonResponse({"success": True, "message": "reply de-verified!"})

        except:
            return JsonResponse({"success": False, "message": "Error verifying reply"})


class ReplieCreateView(PermissionRequiredMixin, LoginRequiredMixin,	CreateView):
    model = Replie
    permission_required = 'replies.add_replie'
    template_name = 'front/discussions/manage/replie/reply_form.html'
    success_url = reverse_lazy('back_replie_list')
    fields = ['post', 'replie_content',
              'image']
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class ReplieUpdateView(PermissionRequiredMixin, LoginRequiredMixin,	UpdateView):
    model = Replie
    permission_required = 'replies.change_replie'
    template_name = 'front/discussions/manage/replie/reply_form.html'
    success_url = reverse_lazy('back_replie_list')
    fields = ['replie_content',
              'image']
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class ReplieDeleteView(PermissionRequiredMixin, LoginRequiredMixin,	DeleteView):
    model = Replie
    template_name = 'front/discussions/manage/replie/delete.html'
    success_url = reverse_lazy('back_replie_list')
    permission_required = 'replies.delete_replie'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class ContactsView(TemplateResponseMixin, View):
    template_name = 'back/administers/contacts_list.html'
    model = Contact

    def get(self,	request):
        site = Home.objects.latest('updated')
        about = About.objects.latest('updated')
        contacts = Contact.objects.all()
        total_posts = Replie.objects.all().count()
        total_courses = Course.objects.all().count()
        total_notes = Note.objects.all().count()
        total_quizzes = Quiz.objects.all().count()
        total_users = User.objects.all().count()
        total_reviews = Review.objects.all().count()
        total_contacts = Contact.objects.all().count()

        return self.render_to_response({'site': site, 'about': about, 'contacts': contacts, 'total_reviews': total_reviews, 'total_posts': total_posts,
                                        'total_courses': total_courses, 'total_notes': total_notes, 'total_quizzes': total_quizzes, 'total_users': total_users, 'total_contacts': total_contacts})

    def post(self,	request, *args, **kwargs):
        pk = request.POST['contact_id']
        try:
            contact = get_object_or_404(
                Contact, id=pk)
            if (contact.seen == 0):
                Contact.objects.filter(pk=pk).update(seen=1)
                return JsonResponse({"success": True, "message": "contact seen!"})
            else:
                Contact.objects.filter(pk=pk).update(seen=0)
                return JsonResponse({"success": True, "message": "contact not seen!"})

        except:
            return JsonResponse({"success": False, "message": "Error making contact as seen "})


class ContactDeleteView(PermissionRequiredMixin, LoginRequiredMixin,	DeleteView):
    model = Contact
    template_name = 'back/administers/contacts/delete.html'
    success_url = reverse_lazy('back_contact_list')
    permission_required = 'contacts.delete_contact'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}
