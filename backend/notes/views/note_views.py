from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from notes.serializers import NoteSerializer, TagSerializer
from notes.services import note_service

# Create your views here.

class NoteListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        tag = request.query_params.get('tag')
        if tag:
            notes = note_service.filter_notes_by_tag(tag=tag, user=user)
        else:
            notes = note_service.list_all_notes(user=user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            title=serializer.validated_data["title"]
            content = serializer.validated_data['content']
            tags = serializer.validated_data.get('tags', [])
            note = note_service.create_note_with_tags(
                note_info={
                    'title': title,
                    'content': content,
                    'tags': tags
                },
                user=request.user
            )
            response_serializer = NoteSerializer(note)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)