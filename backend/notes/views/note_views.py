from rest_framework import viewsets, permissions
from rest_framework.response import Response
from notes.services.note_service import NoteService
from notes.serializers import NoteSerializer

class NoteViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_service(self):
        return NoteService(self.request.user)

    def list(self, request):
        is_archived = str_to_bool(request.query_params.get('is_archived', 'false'))
        service = self.get_service()
        notes = service.list_notes(include_archived=is_archived)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        service = self.get_service()
        note = service.note_repo.get_note(pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        service = self.get_service()
        note = service.create_note(
            title=data.get('title'),
            content=data.get('content'),
            tag_names=data.get('tag_names', []),
            is_archived=data.get('is_archived', False)
        )
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        data = request.data
        service = self.get_service()
        note = service.update_note(
            note_id=pk,
            title=data.get('title'),
            content=data.get('content'),
            tag_names=data.get('tag_names', []),
            is_archived=data.get('is_archived')
        )
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        service = self.get_service()
        service.delete_note(pk)
        return Response(status=204)
    
class ArchivedNoteViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_service(self):
        return NoteService(self.request.user)
    
    def list(self, request):
        service = self.get_service()
        notes = service.list_archived_notes()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    
def str_to_bool(value):
        return str(value).lower() in ['true', '1', 'yes']