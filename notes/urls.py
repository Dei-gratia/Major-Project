from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.NoteListView.as_view(), name='note_list'),
    path('<int:pk>/',
         views.NoteDetailView.as_view(),
         name='note_detail'),
    path('mine/',
         views.ManageNoteListView.as_view(),
         name='manage_note_list'),

    path('create/',
         views.NoteCreateView.as_view(),
         name='note_create'),

    path('<pk>/edit/',
         views.NoteUpdateView.as_view(),
         name='note_edit'),

    path('<pk>/delete/',
         views.NoteDeleteView.as_view(),
         name='note_delete'),
]
