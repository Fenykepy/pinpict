from rest_framework import serializers

from board.models import Board

class BoardSerializer(serializers.ModelSerializer):
    """
    A serializer for Board object with all fields.
    """
    pins = serializers.SerializerMethodField()
    user = serializers.SlugField(
            source="user.slug",
            read_only=True,
    )

    class Meta:
        model = Board
        fields = (
            'date_created',
            'title',
            'slug',
            'description',
            'pin_default_description',
            'n_pins',
            'policy',
            'private',
            'user',
            'order',
            'pins_order',
            'reverse_pins_order',
            'users_can_read',
            'followers',
            'n_followers',
            'pins',
            'cover1', 'cover2', 'cover3',
            'cover4', 'cover5',
        )
        read_only_fields = (
            'followers', 'n_followers', 'user',
            'n_pins', 'slug', 'cover1', 'cover2',
            'cover3', 'cover4', 'cover5',
        )

    def get_pins(self, object):
        return object.get_sorted_pins().only('pk').values_list('pk', flat=True)



class PublicBoardSerializer(BoardSerializer):
    """
    A serializer for Board object with public fields.
    """

    class Meta:
        model= Board
        fields = (
            'title', 'slug', 'description', 'n_pins', 'pins',
            'pin_default_description', 'policy',
        )
        read_only_fields = fields



class AbstractBoardSerializer(BoardSerializer):
    """
    A serializer for Board object with few public fields.
    """
    
    class Meta:
        model = Board
        fields = (
            'title', 'slug', 'n_pins', 'policy', 'cover1',
            'cover2', 'cover3', 'cover4', 'cover5',
        )
        read_only_fields = fields




