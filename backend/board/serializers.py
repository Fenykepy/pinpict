from rest_framework import serializers

from board.models import Board

class BoardSerializer(serializers.ModelSerializer):
    """
    A serializer for Board object with all fields.
    """
    pins = serializers.SerializerMethodField()
    #cover = serializers.SerializerMethodField()

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
            'user',
            'order',
            'pins_order',
            'reverse_pins_order',
            'users_can_read',
            'followers',
            'n_followers',
            'pins',
            #'cover',
        )
        read_only_fields = (
            'user', 'followers', 'n_followers',
            'n_pins', 'slug',
        )

    def get_pins(self, object):
        return object.get_sorted_pins().values_list('pk', flat=True)

    #def get_cover(self, object):
    #    return object.get_main_cover()


class PublicBoardSerializer(BoardSerializer):
    """
    A serializer for Board object with public fields.
    """

    class Meta:
        model= Board
        fields = (
            'title', 'slug', 'description', 'n_pins', 'user',
            'pins',
        )
        read_only_fields = fields



class BoardAbstractSerializer(BoardSerializer):
    """
    A serializer for Board object with few public fields.
    """
    
    class Meta:
        model = Board
        fields = (
            'title', 'slug', 'n_pins', 'user', 'policy'
        )
        read_only_fields = fields




