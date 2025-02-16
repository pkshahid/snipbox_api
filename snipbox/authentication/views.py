from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        """
        - Creates new user using username and password given.
        - Returns error if username is already exist
        - Returns error if there is no username and password in given data
        """

        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            if User.objects.filter(username = username).exists():
                return Response({"error": "Username already exists"}, status = status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username = username, password = password)
            return Response({"message": "User created successfully"}, status = status.HTTP_201_CREATED)
        
        return Response({"message": "Invalid username/password"}, status = status.HTTP_400_BAD_REQUEST)