from rest_framework import serializers
from snippets.models import Snippet


class SnippetSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many = True)


    class Meta:
        model = Snippet
        fields = ['id', 'title', 'note', 'created_at', 'updated_at', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        user = self.context['request'].user
        snippet = Snippet.objects.create(user = user, **validated_data)

        for tag_data in tags_data:

            # Create tag if not already exist. otherwise, get existing tag
            tag, _ = Tag.objects.get_or_create(title = tag_data['title'])

            # Link snippet to tag
            snippet.tags.add(tag)

        return snippet