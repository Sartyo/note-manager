from notes.repositories import note_repository

def create_note_with_tags(title, content, tags, user):
    return note_repository.create_note(title, content, tags, user=user)

def list_all_notes(user):
    return note_repository.get_all_notes(user)

def filter_notes_by_tag(tag, user):
    return note_repository.get_notes_by_tag(tag, user)

def create_new_tag(tag_name, user):
    return note_repository.create_tag(tag_name=tag_name, user=user)

def get_user_tags(user):
    return note_repository.get_all_tags(user=user)

def get_user_tag(tag_name, user):
    return note_repository.get_tag(tag_name=tag_name, user=user)