from notes.models import Note, Tag

def create_note(note_info:dict, user):
    note = Note.objects.create(
        title=note_info["title"],
        content=note_info["content"],
        user=user
    )
    if len(note_info["tags"]) > 0:
        for tag in note_info["tags"]:
            note.tags.add(tag)
    return note

def get_all_notes():
    return Note.objects.prefetch_related('tags', 'user').all()

def get_notes_by_tag(tag, user):
    return Note.objects.filter(tags__name=tag, user=user).prefetch_related('tags', 'user')