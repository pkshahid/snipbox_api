from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from snippets.models import Snippet, Tag
from snippets.serializers import SnippetSerializer, TagSerializer


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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Paginate data
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(queryset, request)

        serializer = self.get_serializer(paginated_data, many=True)

        # Create add detail URL to data
        snippets = [
                {
                    "title" : snippet["title"],
                    "detail_url" : request.build_absolute_uri(
                        reverse('snippets-detail', kwargs={'pk': snippet["id"]})
                        )
                }
                for snippet in serializer.data
            ]
        return paginator.get_paginated_response(snippets)