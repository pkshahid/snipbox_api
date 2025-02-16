from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from snippets.models import Snippet, Tag

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

    def test_update_snippet(self):
        """
        Test updating a snippet
        - Create a snippet
        - Call Snippet update endpoint with inputs
        - Check the response code is 200
        - Check the title of the snippet is same as update input title

        - Call Snippet update endpoint with the valid input
        - Check the response code is 400
        """

        # Positve case
        snippet = Snippet.objects.create(title="Old Title", note="Old Note", user=self.user)
        response = self.client.put(
            f'/api/snippets/{snippet.id}/',
            {"title": "New Title", "note": "New Note", "tags": []},
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        snippet.refresh_from_db()
        self.assertEqual(snippet.title, "New Title")

        # Negative case
        response = self.client.put(
            f'/api/snippets/{snippet.id}/',
            {"title": "New Negative Title"},
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_snippet_list(self):
        """
        Test retrieving snippet list
        - Call Snippet retrieve endpoint
        - Check the response code is 200
        - Check response count is 0.
        - Check reusult length in response is 0.

        - Create a snippet
        - Call Snippet retrieve endpoint
        - Check the response code is 200
        - Check response count is 1.
        - Check reusult length in response is 1.
        """

        # Negative case
        response = self.client.get('/api/snippets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

        # Positive Case
        Snippet.objects.create(
            title="Existing Snippet",
            note="Already exists",
            user=self.user
            )
        response = self.client.get('/api/snippets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)