from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

class NoteAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_note_api(self):
        url = reverse('note-list-create')
        payload = {
            "title": "API Note",
            "content": "Via REST",
            "tag_names": ["api", "test"]
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['tags']), 2)

    def test_filter_note_by_tag_api(self):
        self.client.post(reverse('note-list-create'), {
            "title": "TagTest",
            "content": "Tagged content",
            "tag_names": ["filterme"]
        }, format='json')

        response = self.client.get(reverse('note-list-create') + '?tag=filterme')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "TagTest")