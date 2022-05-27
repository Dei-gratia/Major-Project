from django.contrib import admin
from .models import Course, Module, Content
from django.contrib.contenttypes.admin import GenericTabularInline
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

# Register your models here.


# ====== CONTENT ADMIN ======
class ContentInline(NestedStackedInline):
    model = Content
    extra = 1


# ====== MODULE ADMIN ======
class ModuleInline(NestedStackedInline):
    model = Module
    extra = 1
    inlines = [ContentInline]


# ====== COURSE ADMIN ======
@admin.register(Course)
class CourseAdmin(NestedModelAdmin):
    list_display = ['title', 'subject',	'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug':	('title',)}
    inlines = [ModuleInline]
