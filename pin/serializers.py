from rest_framework import serializers

from pin.models import Pin, Tag
from board.models import Board


class UserSlugRelatedField(serializers.SlugRelatedField):
    """
    Same as serializers.SlugRelatedField, but slug is filtered against request.user
    to get the related object.
    Useful when slug is unique for given user only.
    """

    def get_queryset(self):
        request = self.context.get('request')
        return self.queryset.filter(user=request.user)



class PinSerializer(serializers.ModelSerializer):
    """
    A serializer for Pin object with all fields.
    """
    user = serializers.SlugRelatedField(
            read_only=True,
            slug_field='slug'
    )
    board = UserSlugRelatedField(
            queryset=Board.objects.all(),
            slug_field='slug'
    )

    class Meta:
        model = Pin
        fields =(
            'id', 'url', 'sha1', 'source_file', 'source_file_url', 'source_domain',
            'source', 'date_created', 'date_updated', 'description', 'board',
            'added_via', 'user', 'private', 'owner_rate', 'likes','n_likes',
        )
        read_only_fields = (
            'id', 'user', 'n_likes', 'likes', 'private', 'added_via', 'date_created',
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
