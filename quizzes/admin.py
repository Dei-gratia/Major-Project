from django.contrib import admin
from .models import Question, Quiz

# Register your models here.


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'school_level', 'subject', 'created']
    list_filter = ['created', 'school_level', 'subject']
    search_fields = ['title', 'description']

    inlines = [
        QuestionInline,
    ]
