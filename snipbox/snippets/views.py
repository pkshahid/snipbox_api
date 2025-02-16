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
        """ Lists snippets and respective detail url """
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

    def destroy(self, request, *args, **kwargs):
        """ Deletes specific snippet and return remaining snippets """
        instance = self.get_object()
        instance.delete()             #Deletes selected snippet instance

        # Fetch remaining snippets
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many = True)
        return Response(
                        {
                            "message": "Snippet deleted successfully",
                            "available_snippets": serializer.data
                        },
                        status = status.HTTP_204_NO_CONTENT
                    )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Handles create, retreive, update and destroy operations on Tags.
    - Overrided retrieve() method to return snippets related to specific tags
    """
    queryset = Tag.objects.all().order_by("-id")
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Fetch all snippets related to the given tag
        related_snippets = instance.snippet_set.filter(user = request.user)

        # Paginate data
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(related_snippets, request)

        serializer = SnippetSerializer(paginated_data, many = True)

        # Return paginated data response
        return paginator.get_paginated_response({
            "tag" : instance.title,
            "snippets": serializer.data,
        })