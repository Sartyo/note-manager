from notes.models import Note, Tag
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name'
        ]

class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_names = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )

    class Meta:
        model = Note
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'tags',
            'tag_names'
        ]
    
    def create(self, validated_data):
        tag_names = validated_data.pop('tag_names', [])
        note = Note.objects.create(**validated_data)
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            note.tags.add(tag)
        return note