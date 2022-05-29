from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count
from .forms import PostFormSet
from .models import DiscussionTopic, Post, Replie
from users.models import Profile
from main.models import Subject, SchoolLevel, Home, About
from django.views.generic.detail import DetailView
from main.mixins import OwnerEditMixin, OwnerMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.views.generic.edit import CreateView,	UpdateView,	DeleteView
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

# Create your views here.


class DiscussionTopicListView(TemplateResponseMixin,	View):
    model = DiscussionTopic
    template_name = 'front/discussions/topic/list.html'

    def get(self,	request, school_level=None,	subject=None):
        subjects = Subject.objects.annotate(
            total_topics=Count('discussion_topics'))
        school_levels = SchoolLevel.objects.annotate(
            total_topics=Count('discussion_topics'))
        discussion_topics = DiscussionTopic.objects.annotate(
            total_posts=Count('posts'))
        latest = Post.objects.all().order_by('-date')[:5]

        if school_level:
            school_level = get_object_or_404(Subject, slug=subject)
            discussion_topics = discussion_topics.filter(
                school_level=school_level)

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            discussion_topics = discussion_topics.filter(subject=subject)

        return self.render_to_response({'subjects':	subjects,
                                        'school_level': school_level,
                                        'subject':	subject,
                                        'discussion_topics':	discussion_topics,
                                        'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated'),
                                        'latest': latest})


class DiscussionTopicDetailView(DetailView):
    model = DiscussionTopic
    template_name = 'front/discussions/topic/detail.html'

    def get_context_data(self,	**kwargs):
        context = super(DiscussionTopicDetailView,
                        self).get_context_data(**kwargs)
        context['site'] = Home.objects.latest('updated')
        context['about'] = About.objects.latest('updated')
        print(self.object.title)
        context['discussion_topic'] = self.object
        context['latest'] = Post.objects.all().order_by('-date')[:5]
        return context

    def post(self, request, *args, pk, **kwargs):
        userprofile = request.user.profile
        print(args, kwargs, pk)
        print(userprofile, '\n'*5)
        comment = request.POST['comment']
        rating = request.POST['input-1']
        print(rating, comment, userprofile)
        discussion = get_object_or_404(
            DiscussionTopic, id=pk, owner=request.user)
        print(discussion)
        user_review = discussion.reviews.filter(user=request.user)
        print(user_review)

        if comment == "" and rating == "":

            return JsonResponse({"success": False, "message": "Please provide a rating or comment"})
        if user_review:
            discussion_total_ratings = float(discussion.total_ratings) -\
                float(user_review[0].rate_value) + float(rating)
            discussion_num_ratings = float(discussion.num_ratings)
            # Review.objects.filter(user=user_review.user).update(rate_value=rating, comment=comment)
            user_review.update(rate_value=rating, comment=comment)
            print(user_review[0])
            print(discussion_num_ratings, discussion_total_ratings)
        else:
            review = Review(content_object=discussion, user=request.user,
                            rate_value=rating, comment=comment)
            review.save()
            discussion_num_ratings = float(discussion.num_ratings) + 1
            discussion_total_ratings = float(
                discussion.total_ratings) + float(rating)

        print(discussion_num_ratings, discussion_total_ratings)
        DiscussionTopic.objects.filter(pk=pk).update(total_ratings=discussion_total_ratings,
                                                     num_ratings=discussion_num_ratings)

        return JsonResponse({"success": True, "message": "review saved"})


class OwnerDiscussionMixin(OwnerMixin, LoginRequiredMixin):
    model = DiscussionTopic
    fields = ['school_level', 'subject',
              'title', 'cover_img', 'number_of_posts']
    success_url = reverse_lazy('manage_discussion_topic_list')


class OwnerDiscussionEditMixin(OwnerDiscussionMixin,	OwnerEditMixin):
    fields = ['school_level', 'subject', 'title',
              'cover_img', ]
    success_url = reverse_lazy('manage_discussion_topic_list')
    template_name = 'front/discussions/manage/topic/form.html'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class ManageDiscussionListView(OwnerDiscussionMixin,	ListView):
    template_name = 'front/discussions/manage/topic/list.html'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class DiscussionCreateView(PermissionRequiredMixin, OwnerDiscussionEditMixin,	CreateView):
    permission_required = 'discussions.add_discussion'


class DiscussionUpdateView(PermissionRequiredMixin, OwnerDiscussionEditMixin,	UpdateView):
    permission_required = 'discussions.change_discussion'


class DiscussionDeleteView(PermissionRequiredMixin, OwnerDiscussionMixin,	DeleteView):
    template_name = 'front/discussions/manage/topic/delete.html'
    success_url = reverse_lazy('manage_discussion_topic_list')
    permission_required = 'discussions.delete_discussion'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class DiscussionPostUpdateView(TemplateResponseMixin,	View):
    template_name = 'front/discussions/manage/post/formset.html'
    discussion_topic = None

    def get_formset(self,	data=None):
        return PostFormSet(instance=self.discussion_topic, data=data)

    def dispatch(self,	request,	pk):
        self.discussion_topic = get_object_or_404(
            DiscussionTopic, id=pk, owner=request.user)
        return super(DiscussionPostUpdateView, self).dispatch(request,	pk)

    def get(self,	request,	*args,	**kwargs):
        formset = self.get_formset()
        return self.render_to_response({'discussion_topic':	self.discussion_topic, 'formset':	formset, 'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated')})

    def post(self,	request,	*args,	**kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_discussion_topic_list')
        return self.render_to_response({'discussion_topic':	self.discussion_topic, 'formset':	formset, 'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated')})


class DiscussionPostListView(TemplateResponseMixin,	View):
    template_name = 'front/discussions/topic/post_list.html'

    def get(self,	request,	topic_id):
        discussion_topic = get_object_or_404(
            DiscussionTopic, id=topic_id, owner=request.user)
        return self.render_to_response({'topic':	discussion_topic, 'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated')})

    def post(self,	request,	*args, topic_id,	**kwargs):
        discussion_topic = get_object_or_404(
            DiscussionTopic, id=topic_id, owner=request.user)
        post_title = request.POST.get('post_title')
        post_content = request.POST.get('post_content')
        if post_title == "" and post_content == "":

            return JsonResponse({"success": False, "message": "Both post title and post content can not be empty!!"})
        new_post = Post(owner=request.user, title=post_title,
                        post_content=post_content, discussion_topic=discussion_topic)

        new_post.save()

        return JsonResponse({"success": True, "message": "Your post has been posted!"})


class DiscussionPostDetailView(TemplateResponseMixin,	View):
    template_name = 'front/discussions/topic/post_detail.html'

    def get(self,	request,	topic_id, post_id):
        discussion_topic = get_object_or_404(
            DiscussionTopic, id=topic_id, owner=request.user)
        post = get_object_or_404(
            Post, id=post_id, owner=request.user)
        return self.render_to_response({'topic':	discussion_topic, 'post': post, 'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated')})

    def post(self,	request,	*args, topic_id, post_id,	**kwargs):
        discussion_topic = get_object_or_404(
            DiscussionTopic, id=topic_id, owner=request.user)
        post = get_object_or_404(
            Post, id=post_id, owner=request.user)
        replie_content = request.POST.get('reply_content')
        if replie_content == "":

            return JsonResponse({"success": False, "message": "Reply can not be empty!!"})
        reply = Replie(user=request.user,
                       replie_content=replie_content, post=post)
        reply.save()

        return JsonResponse({"success": True, "message": "Your reply has been submitted!"})
