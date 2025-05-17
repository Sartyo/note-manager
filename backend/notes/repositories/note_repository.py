from notes.models import Note, Tag

def create_note(title, content, tag_names, user):
    note = Note.objects.create(title=title, content=content, user=user)
    for name in tag_names:
        tag, _ = Tag.objects.get_or_create(name=name, user=user)
        note.tags.add(tag)
    return note

def get_all_notes(user):
    return Note.objects.filter(user=user).prefetch_related('tags')

def get_notes_by_tag(tag, user):
    return Note.objects.filter(tags__name=tag, user=user).prefetch_related('tags', 'user')