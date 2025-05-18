from django.db import transaction
from notes.repositories.tag_repository import TagRepository

class TagService:
    def __init__(self, user):
        self.user = user
        self.tag_repo = TagRepository(user)

    def list_tags(self):
        return self.tag_repo.list_tags()

    def get_tag(self, tag_id):
        return self.tag_repo.get_tag(tag_id)

    def create_tag(self, name):
        return self.tag_repo.create_tag(name)

    def update_tag(self, tag_id, name):
        return self.tag_repo.update_tag(tag_id, name)
    
    def delete_tag(self, tag_id):
        return self.tag_repo.delete_tag(tag_id)