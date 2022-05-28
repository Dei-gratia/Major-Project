from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count
from .forms import QuestionFormSet
from .models import Question, Quiz
from users.models import Review, Profile
from main.models import Subject, SchoolLevel, Home, About
from django.views.generic.detail import DetailView
from main.mixins import OwnerEditMixin, OwnerMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.views.generic.edit import CreateView,	UpdateView,	DeleteView
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

# Create your views here.


class QuizListView(TemplateResponseMixin,	View):
    model = Quiz
    template_name = 'front/quizzes/quiz/list.html'

    def get(self,	request,	subject=None):
        subjects = Subject.objects.annotate(total_courses=Count('quizzes'))
        quizzes = Quiz.objects.annotate(total_reviews=Count('reviews'))
        latest = Quiz.objects.all().order_by('-created')[:5]

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            quizzes = quizzes.filter(subject=subject)

        return self.render_to_response({'subjects':	subjects,
                                        'subject':	subject,
                                        'quizzes':	quizzes,
                                        'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated'),
                                        'latest': latest})


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'front/quizzes/quiz/detail.html'

    def get_context_data(self,	**kwargs):
        context = super(QuizDetailView, self).get_context_data(**kwargs)
        context['site'] = Home.objects.latest('updated')
        context['about'] = About.objects.latest('updated')
        context['latest'] = Quiz.objects.all().order_by('-created')[:5]
        return context

    def post(self, request, *args, pk, **kwargs):
        userprofile = request.user.profile
        print(args, kwargs, pk)
        print(userprofile, '\n'*5)
        comment = request.POST['comment']
        rating = request.POST['input-1']
        print(rating, comment, userprofile)
        quiz = get_object_or_404(
            Quiz, id=pk, owner=request.user)
        print(quiz)
        user_review = quiz.reviews.filter(user=request.user)
        print(user_review)

        if comment == "" and rating == "":

            return JsonResponse({"success": False, "message": "Please provide a rating or comment"})
        if user_review:
            quiz_total_ratings = float(quiz.total_ratings) -\
                float(user_review[0].rate_value) + float(rating)
            quiz_num_ratings = float(quiz.num_ratings)
            # Review.objects.filter(user=user_review.user).update(rate_value=rating, comment=comment)
            user_review.update(rate_value=rating, comment=comment)
            print(user_review[0])
            print(quiz_num_ratings, quiz_total_ratings)
        else:
            review = Review(content_object=quiz, user=request.user,
                            rate_value=rating, comment=comment)
            review.save()
            quiz_num_ratings = float(quiz.num_ratings) + 1
            quiz_total_ratings = float(quiz.total_ratings) + float(rating)

        print(quiz_num_ratings, quiz_total_ratings)
        Quiz.objects.filter(pk=pk).update(total_ratings=quiz_total_ratings,
                                          num_ratings=quiz_num_ratings)

        return JsonResponse({"success": True, "message": "review saved"})


class OwnerQuizMixin(OwnerMixin, LoginRequiredMixin):
    model = Quiz
    fields = ['school_level', 'subject',
              'title', 'description', 'tags']
    success_url = reverse_lazy('manage_quiz_list')


class OwnerQuizEditMixin(OwnerQuizMixin,	OwnerEditMixin):
    fields = ['school_level', 'subject', 'title',
              'description', 'tags']
    success_url = reverse_lazy('manage_quiz_list')
    template_name = 'front/quizzes/manage/quiz/form.html'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class ManageQuizListView(OwnerQuizMixin,	ListView):
    template_name = 'front/quizzes/manage/quiz/list.html'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class QuizCreateView(PermissionRequiredMixin, OwnerQuizEditMixin,	CreateView):
    permission_required = 'quizzes.add_quiz'


class QuizUpdateView(PermissionRequiredMixin, OwnerQuizEditMixin,	UpdateView):
    permission_required = 'quizzes.change_quiz'


class QuizDeleteView(PermissionRequiredMixin, OwnerQuizMixin,	DeleteView):
    template_name = 'front/quizzes/manage/quiz/delete.html'
    success_url = reverse_lazy('manage_quiz_list')
    permission_required = 'quizzes.delete_quiz'
    extra_context = {'site': Home.objects.latest('updated'),
                     'about': About.objects.latest('updated')}


class QuizQuestionUpdateView(TemplateResponseMixin,	View):
    template_name = 'front/courses/manage/module/formset.html'
    quiz = None

    def get_formset(self,	data=None):
        return QuestionFormSet(instance=self.quiz, data=data)

    def dispatch(self,	request,	pk):
        self.quiz = get_object_or_404(Quiz, id=pk, owner=request.user)
        return super(QuizQuestionUpdateView, self).dispatch(request,	pk)

    def get(self,	request,	*args,	**kwargs):
        formset = self.get_formset()
        return self.render_to_response({'quiz':	self.quiz, 'formset':	formset, 'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated')})

    def post(self,	request,	*args,	**kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_quiz_list')
        return self.render_to_response({'quiz':	self.quiz, 'formset':	formset, 'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated')})


class QuestionOrderView(CsrfExemptMixin, JsonRequestResponseMixin, 	View):
    def post(self,	request):
        for id,	order in self.request_json.items():
            Question.objects.filter(id=id,
                                    quiz__owner=request.user).update(order=order)
        return self.render_json_response({'saved':	'OK'})


class QuizQuestionListView(TemplateResponseMixin,	View):
    template_name = 'front/quizzes/quiz/question_list.html'

    def get(self,	request,	quiz_id):
        quiz = get_object_or_404(
            Quiz, id=quiz_id, owner=request.user)
        return self.render_to_response({'quiz':	quiz, 'site': Home.objects.latest('updated'),
                                        'about': About.objects.latest('updated')})

    def post(self,	request,	*args, quiz_id,	**kwargs):
        quiz = get_object_or_404(
            Quiz, id=quiz_id, owner=request.user)
        questions = quiz.questions.all()
        correct = 0
        wrong = 0
        skipped = 0
        result = ['0']
        for question in questions:
            result.append(request.POST.get(question.question))
            if question.correct_option == request.POST.get(question.question):
                correct += 1
            elif (request.POST.get(question.question) == None):
                skipped += 1
            else:
                wrong += 1
        half = float(quiz.number_of_questions)/2
        print(correct, half)
        if correct >= half:
            message = "Cograts, you passed!🥳🥳🥳"
        elif skipped >= half:
            message = '😞Fail, try attempting all question next time'
        else:
            message = "😞Less than half, dont worry you can review your answer and try again later😅"

        return render(request, 'front/quizzes/quiz/result.html',
                      {'quiz':	quiz,  'site': Home.objects.latest('updated'),
                       'about': About.objects.latest('updated'),
                       'message': message,
                       'result': result,
                       'correct': correct,
                       'wrong': wrong,
                       'skipped': skipped})
