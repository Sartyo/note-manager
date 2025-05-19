from django.db import transaction
from notes.repositories.tag_repository import TagRepository
from notes.repositories.note_repository import NoteRepository

class NoteService:
    def __init__(self, user):
        self.user = user
        self.note_repo = NoteRepository(user)
        self.tag_repo = TagRepository(user)

    def list_notes(self, include_archived):
        return self.note_repo.list_notes(include_archived)

    def get_note(self, note_id):
        return self.note_repo.get_note(note_id)

    @transaction.atomic
    def create_note(self, title, content, tag_names=None, is_archived=False):
        note = self.note_repo.create_note(title=title, content=content, is_archived=is_archived)
        if tag_names:
            tags = [self.tag_repo.get_or_create_tag(name) for name in tag_names]
            note.tags.set(tags)
        return note

    @transaction.atomic
    def update_note(self, note_id, title=None, content=None, tag_names=None, is_archived=None):
        note = self.note_repo.get_note(note_id)
        updated_data = {}
        if title is not None:
            updated_data['title'] = title
        if content is not None:
            updated_data['content'] = content
        if is_archived is not None:
            updated_data['is_archived'] = is_archived

        note = self.note_repo.update_note(note, **updated_data)

        if tag_names is not None:
            tags = [self.tag_repo.get_or_create_tag(name) for name in tag_names]
            note.tags.set(tags)

        return note

    def delete_note(self, note_id):
        note = self.note_repo.get_note(note_id)
        self.note_repo.delete_note(note)

    def archive_note(self, note_id):
        return self.update_note(note_id, is_archived=True)

    def unarchive_note(self, note_id):
        return self.update_note(note_id, is_archived=False)
    
    def list_archived_notes(self):
        return self.note_repo.list_archived_notes()