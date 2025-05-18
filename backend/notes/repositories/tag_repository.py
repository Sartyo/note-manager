from notes.models import Tag
from django.shortcuts import get_object_or_404

class TagRepository:
    def __init__(self, user):
        self.user = user

    def list_tags(self):
        return Tag.objects.filter(user=self.user)

    def get_tag(self, tag_id):
        return get_object_or_404(Tag, id=tag_id, user=self.user)

    def get_or_create_tag(self, name):
        tag, _ = Tag.objects.get_or_create(name=name, user=self.user)
        return tag

    def create_tag(self, name):
        return Tag.objects.create(name=name, user=self.user)

    def update_tag(self, tag_id, name):
        tag = self.get_tag(tag_id)
        tag.name = name
        tag.save()
        return tag

    def delete_tag(self, tag_id):
        tag = self.get_tag(tag_id)
        tag.delete()