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
            'tag_names',
            'is_archived'
        ]

    def create(self, validated_data):
        print("Validated data:", validated_data)
        tag_names = validated_data.pop('tag_names', [])
        user = self.context['request'].user

        # Now validated_data contains title, content, is_archived (but NOT tags)
        note = Note.objects.create(user=user, **validated_data)

        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name, user=user)
            note.tags.add(tag)

        return note