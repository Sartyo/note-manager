from django.test import TestCase
from django.contrib.auth.models import User
from notes.services import note_service

class NoteServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="serviceuser", password="pass")

    def test_create_and_retrieve_note(self):
        note_service.create_note_with_tags("Meeting", "Zoom", ["remote"], self.user)
        notes = note_service.list_all_notes(self.user)
        self.assertEqual(len(notes), 1)

    def test_filter_notes_by_tag(self):
        note_service.create_note_with_tags("Log", "Daily entry", ["journal"], self.user)
        filtered = note_service.filter_notes_by_tag("journal", self.user)
        self.assertEqual(len(filtered), 1)