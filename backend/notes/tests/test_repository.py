from django.test import TestCase
from django.contrib.auth.models import User
from notes.models import Note, Tag
from notes.repositories import note_repository

class NoteRepositoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="repo_user", password="testpass")

    def test_create_note_with_tags(self):
        note = note_repository.create_note("Test Note", "Content", ["work", "urgent"], self.user)
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.tags.count(), 2)
        self.assertTrue(Tag.objects.filter(name="work", user=self.user).exists())

    def test_get_all_notes(self):
        note_repository.create_note("Note A", "Content A", ["tag1"], self.user)
        notes = note_repository.get_all_notes(self.user)
        self.assertEqual(len(notes), 1)

    def test_get_notes_by_tag(self):
        note_repository.create_note("Tagged Note", "Tag test", ["code"], self.user)
        notes = note_repository.get_notes_by_tag("code", self.user)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].title, "Tagged Note")