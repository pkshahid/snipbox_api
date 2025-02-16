from rest_framework import serializers
from snippets.models import Snippet, Tag


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

    def update(self, instance, validated_data):
        """
        Overrided update() method of serializer to implement custom logic
        - Update field value other than tags
        - Add new tags if any
        - Remove existing tags of snippet if it's not present in update data
        - Returns Updated snippet instance
        """
        for attr, value in validated_data.items():
            if not attr == 'tags':
                setattr(instance, attr, value)  # Dynamically update fields
        instance.save()
        instance.refresh_from_db()
        deleted_tags = {tag.title:tag.id for tag in instance.tags.all()}
        if ('tags' in validated_data and validated_data['tags']):
            for tag in validated_data['tags']:
                if tag['title']:
                    deleted_tags.pop(tag['title'],None)
                    new_tag, _ = Tag.objects.get_or_create(title = tag['title'])
                    instance.tags.add(new_tag)
        if deleted_tags:

            for tag,id in deleted_tags.items():
                instance.tags.remove(id)
            instance.refresh_from_db()
        return instance

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
