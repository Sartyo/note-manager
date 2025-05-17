from notes.repositories import note_repository

def create_note_with_tags(note_info:dict, user):
    return note_repository.create_note(note_info=note_info, user=user)

def list_all_notes(user):
    return note_repository.get_all_notes(user)

def filter_notes_by_tag(tag, user):
    return note_repository.get_notes_by_tag(tag, user)