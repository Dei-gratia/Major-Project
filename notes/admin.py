from django.contrib import admin
from .models import Note
from users.models import Review
# Register your models here.


# ====== NOTEADMIN =====
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'school_level', 'subject',	'created']
    list_filter = ['created', 'school_level', 'subject']
    search_fields = ['title', 'description', 'body']
