from django.urls import path
from notes.views import note_views

urlpatterns = [
    path('notes/', note_views.NoteListCreateView.as_view(), name='note-list-create'),
]