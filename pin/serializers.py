from rest_framework import serializers

from pin.models import Pin, Tag



class PinSerializer(serializers.ModelSerializer):
    """
    A serializer for Pin object with all fields.
    """
    user = serializers.SlugRelatedField(
            read_only=True,
            slug_field='slug'
    )
    board = serializers.SlugRelatedField(
            read_only=True,
            slug_field='slug'
    )

    class Meta:
        model = Pin
        fields =(
            'id', 'url', 'sha1', 'source_file', 'source_file_url', 'source_domain',
            'source', 'date_created', 'date_updated', 'description', 'board',
            'added_via', 'user', 'policy', 'owner_rate', 'likes','n_likes',
        )
        read_only_fields = (
            'user', 'n_likes', 'likes', 'policy', 'added_via', 'date_created',
            'date_updated', 'sha1', 'source_domain',
        )



class TagSerializer(serializers.ModelSerializer):
    """
    A serializer with all tags data.
    """
    class Meta:
        model = Tag
        fields = ('name')



class UrlSerializer(serializers.Serializer):
    """
    A serializer for url.
    """
    url = serializers.URLField()
    full_search = serializers.BooleanField(default=False)


class ScannedPictureSerializer(serializers.Serializer):
    """
    A serializer for pictures found in html scan.
    """
    src = serializers.URLField()
    description = serializers.CharField(allow_blank=True)
