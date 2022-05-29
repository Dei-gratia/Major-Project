from django.contrib import admin
from .models import DiscussionTopic, Post, Replie
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

# Register your models here.


class ReplieInline(NestedStackedInline):
    model = Replie
    extra = 0


class PostInline(NestedStackedInline):
    model = Post
    extra = 0
    inlines = [
        ReplieInline,
    ]


@admin.register(DiscussionTopic)
class DiscussionAdmin(NestedModelAdmin):
    list_display = ['title', 'school_level', 'subject',	'date']
    list_filter = ['date', 'school_level', 'subject']
    search_fields = ['title', 'description', 'body']
    inlines = [
        PostInline,
    ]
