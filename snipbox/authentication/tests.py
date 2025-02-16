from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class AuthAPITestCase(APITestCase):

    def setUp(self):
        """Setup test user"""

        self.user = User.objects.create_user(username="testuser", password="password123")
        self.token = RefreshToken.for_user(self.user)

    def test_login(self):
        """
        Test user login and token retrieval
        - Call the login endpoint with valid user credntials
        - Check the response code is 200.
        - Check the response has access token.
        - Check the response has refresh token

        - Call the login endpoint with invalid credntials.
        - Check the response code is 400
        """

        # Positive case
        response = self.client.post('/api/auth/login',{
            "username": "testuser", "password": "password123"
            }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        response = self.client.post('/api/auth/login', {
            "username": "", "password": "password123"
            }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token(self):
        """
        Test token refresh
        - Call token refresh endpoint with a valid refresh token
        - Check the response code is 200
        - Check the response has access token
        - Check the response has refresh token

        - Call the token refresh endpoint with invalid refresh token
        - Check the response code is 401
        """

        # Positve case
        response = self.client.post('/api/auth/token/refresh/', {
            "refresh": str(self.token)
            }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Negative case
        response = self.client.post('/api/auth/token/refresh/', {
            "refresh": "abc21441"
            }, format='json')
            
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)