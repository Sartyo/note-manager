from notes.models import Note

class NoteRepository:
    def __init__(self, user):
        self.user = user

    def list_notes(self, include_archived):
        queryset = Note.objects.filter(user=self.user)
        queryset = queryset.filter(is_archived=include_archived)
        return queryset

    def get_note(self, note_id):
        return Note.objects.get(id=note_id, user=self.user)

    def create_note(self, **kwargs):
        return Note.objects.create(user=self.user, **kwargs)

    def update_note(self, note, **kwargs):
        for key, value in kwargs.items():
            setattr(note, key, value)
        note.save()
        return note

    def delete_note(self, note):
        note.delete()

    def list_archived_notes(self):
        queryset = Note.objects.filter(user=self.user, is_archived=True)
        return queryset
    