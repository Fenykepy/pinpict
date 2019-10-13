from rest_framework import serializers

from pin.models import Pin

class PinSerializer(serializers.ModelSerializer):
    """
    A serializer for Pin object with all fields.
    """

    class Meta:
        model = Pin




