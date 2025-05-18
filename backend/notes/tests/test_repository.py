from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from notes.models import Note, Tag
from notes.repositories.note_repository import NoteRepository
from notes.services.note_service import NoteService
from notes.repositories.tag_repository import TagRepository

User = get_user_model()

class NoteServiceTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="pass123")
        self.user2 = User.objects.create_user(username="bob", password="pass123")

    def test_users_can_create_notes_with_same_tag_name(self):
        note_service1 = NoteService(user=self.user1)
        note_service2 = NoteService(user=self.user2)

        # Both users create a note with the tag "Work"
        note1 = note_service1.create_note(
            title="Note from Alice",
            content="Content A",
            tag_names=["Work"]
        )

        note2 = note_service2.create_note(
            title="Note from Bob",
            content="Content B",
            tag_names=["Work"]
        )

        # Assertions
        self.assertEqual(note1.tags.first().name, "Work")
        self.assertEqual(note2.tags.first().name, "Work")
        self.assertNotEqual(note1.tags.first().id, note2.tags.first().id)

        self.assertEqual(note1.user, self.user1)
        self.assertEqual(note2.user, self.user2)
        self.assertEqual(Tag.objects.count(), 2)  # Two "Work" tags, one per user
        self.assertEqual(Note.objects.count(), 2)

class TagRepositoryTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

    def test_users_can_have_same_tag_name(self):
        repo1 = TagRepository(user=self.user1)
        repo2 = TagRepository(user=self.user2)

        tag1 = repo1.get_or_create_tag('Work')
        tag2 = repo2.get_or_create_tag('Work')

        self.assertEqual(tag1.name, 'Work')
        self.assertEqual(tag2.name, 'Work')
        self.assertNotEqual(tag1.user, tag2.user)
        self.assertEqual(Tag.objects.count(), 2)

    def test_same_tag_name_different_users(self):
        user1 = User.objects.create_user(username='user1', password='test')
        user2 = User.objects.create_user(username='user2', password='test')

        tag1 = Tag.objects.create(name='Work', user=user1)
        tag2 = Tag.objects.create(name='Work', user=user2)

        self.assertNotEqual(tag1.id, tag2.id)