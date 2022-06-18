from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='admin_dashboard'),
    path('notes/', views.NotesView.as_view(), name='back_note_list'),
    path('notes/<pk>/delete', views.NoteDeleteView.as_view(),
         name='back_note_delete'),
    path('notes/<pk>/edit', views.NoteUpdateView.as_view(),
         name='back_note_edit'),

]
