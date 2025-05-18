from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notes.views.note_views import NoteViewSet, ArchivedNoteViewSet
from notes.views.tag_views import TagViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'archived-notes', ArchivedNoteViewSet, basename='archived_notes')

urlpatterns = [
    path('', include(router.urls)),
]