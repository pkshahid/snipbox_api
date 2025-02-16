from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetViewSet(viewsets.ModelViewSet):

    """
    Handles create, retreive, update and destroy operations on Snippets.
    And returns 400 Bad request response if there is any error.
    - Overrided get_queryset() method to retreive only user specific data.
    - Overrided list() method to include detail_url for respective snippets
    - Overrided destroy() method to return available snippets on delete
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)