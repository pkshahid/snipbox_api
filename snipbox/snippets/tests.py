from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from snippets.models import Snippet

class SnippetAPITestCase(APITestCase):

    def setUp(self):
        """
        Setup
        - Create testuser and authenticate the user
        - Create a tag
        - Create test snippet data
        """
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'password123'
            )

        self.client.force_authenticate(user = self.user)
        self.tag = Tag.objects.create(title = "Django")

        self.positive_snippet_data = {
            "title": "Test Snippet",
            "note": "This is a positive test snippet.",
            "tags": [{"title": "Django"}]
        }

        self.negative_snippet_data = {
            "note": "This is a negative test snippet.",
            "tags": [{"title": "Django"}]
        }

    def test_create_snippet(self):
        """
        Test creating a new snippet
        - Call Snippet create endpoint with valid input
        - Check the response code is 201
        - Check snippet is created.
        - Check created snippet title is same as given input

        - Call Snippet create endpoint with invalid input
        - Check the response code is 400
        - Check any snippet is not created with given input
        """

        # Positive case test
        response = self.client.post('/api/snippets/', self.positive_snippet_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Snippet.objects.count(), 1)
        self.assertEqual(Snippet.objects.first().title, self.positive_snippet_data['title'])

        # Negative case test
        response = self.client.post('/api/snippets/', self.negative_snippet_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Snippet.objects.filter(note = self.negative_snippet_data["note"]).exists())
