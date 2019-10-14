from rest_framework import serializers

from pin.models import Pin, Tag

class PinSerializer(serializers.ModelSerializer):
    """
    A serializer for Pin object with all fields.
    """

    class Meta:
        model = Pin


class TagSerializer(serializers.ModelSerializer):
    """
    A serializer with all tags data.
    """
    class Meta:
        model = Tag
        fields = ('name')


