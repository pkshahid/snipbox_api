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

    def test_get_snippet_detail(self):
        """
        Test retrieving a specific snippet
        - Call Snippet detail endpoint with invalid ID
        - Check the response code is 400

        - Create a snippet
        - Call Snippet detail endpoint with the valid ID
        - Check the response code is 200
        - Check title of retrieved snippet in response is same as created.
        """

        # Nagative case
        response = self.client.get(f'/api/snippets/{1}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Positive case
        snippet = Snippet.objects.create(title="Detail Test", note="Testing detail", user=self.user)
        response = self.client.get(f'/api/snippets/{snippet.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], snippet.title)

    def test_tag_create(self):
        """
        Test Tag creation and linking
        - Create a snippet with an existing tag and new tag
        - Check the response code is 201
        - Check total tags count is still 2
        - Check the new tag has created
        - Check the existing tag count, verify that duplicate is not created.
        - Check the tags count of the snippet is 2
        """
        self.positive_snippet_data['tags'].append({"title": "Test"})
        response = self.client.post('/api/snippets/', self.positive_snippet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(),2)
        self.assertTrue(Tag.objects.filter(title="Test").exists())
        self.assertEqual(Tag.objects.filter(title="Django").count(),1)
        self.assertEqual(Snippet.objects.get(title=self.positive_snippet_data["title"]).tags.count(),2)

    def test_delete_snippet(self):
        """
        Test deleting a snippet
        - Create a snippet
        - Call Snippet delete endpoint with ID of the snippet
        - Check the response code is 204
        - Check the initially created snippet deleted or not

        - Call Snippet delete endpoint with the invalid ID
        - Check the response code is 404
        """

        # Positive case
        snippet = Snippet.objects.create(title = "To be deleted", note = "Delete me", user = self.user)
        response = self.client.delete(f'/api/snippets/{snippet.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 0)

        # Negative case
        response = self.client.delete(f'/api/snippets/{snippet.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TagAPITestCase(APITestCase):

    def setUp(self):
        """Setup test user and authentication"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.tag = Tag.objects.create(title="Test_Tag")
        self.snippet_data = {
            "title": "Test Snippet",
            "note": "This is a positive test snippet.",
            "tags": [{"title": "Test_Tag"}]
        }

    def test_list_tags(self):
        """
        Test retrieving all tags
        - Call tags list endpoint
        - Check the response code is 200
        - Check response count is 1
        - Check response data length is 1
        """

        response = self.client.get('/api/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)