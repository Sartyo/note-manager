from rest_framework import viewsets, permissions
from rest_framework.response import Response
from notes.models import Tag
from notes.serializers import TagSerializer
from notes.services.tag_service import TagService

class TagViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_service(self):
        return TagService(self.request.user)

    def list(self, request):
        service = self.get_service()
        tags = service.list_tags()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        service = self.get_service()
        tag = service.get_tag(pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def create(self, request):
        name = request.data.get('name')
        service = self.get_service()
        tag = service.create_tag(name)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        name = request.data.get('name')
        service = self.get_service()
        tag = service.update_tag(pk, name)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        service = self.get_service()
        service.delete_tag(pk)
        return Response(status=204)