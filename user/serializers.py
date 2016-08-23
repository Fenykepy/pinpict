from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    A serializer for User object with all fields.
    """
    # set required to false else with browsable api
    # each put with empty file erase existing one
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = (
                'pk',
                'url',
                'username',
                'first_name',
                'last_name',
                'email',
                'is_staff',
                'is_active',
                'avatar',
                'website',
                'facebook_link',
                'flickr_link',
                'px500_link',
                'twitter_link',
                'gplus_link',
                'pinterest_link',
                'vk_link',
                'instagram_link'
                'n_followers',
                'n_following',
                'n_likes',
                'n_public_likes',
                'n_pins',
                'n_public_pins',
                'n_boards',
                'n_public_boards',
                'n_unread_notifications',
                'mail_user_follower',
                'mail_board_follower',
                'mail_following_add_pin',
                'mail_following_add_board',
                'mail_repinned',
                'mail_allow_read',
                'mail_following_liked_pin',
                'mail_pin_like',
        )

        def create(self, validated_data):
            return User.objects.create(**validated_data)

        def update(self, instance, validated_data)
            password = validated_data.get('password', None)

            if password:
                instance.set_password(password)
                instance.save()

            return instance



class SafeUserSerializer(UserSerializer):
    """
    A serialiser which allow writting on safe datas only.
    Used by corresponding user itself.
    """

    class Meta:
        model = User
        fields = (
                'pk',
                'url',
                'username',
                'first_name',
                'last_name',
                'email',
                'is_staff',
                'is_active',
                'avatar',
                'website',
                'facebook_link',
                'flickr_link',
                'px500_link',
                'twitter_link',
                'gplus_link',
                'pinterest_link',
                'vk_link',
                'instagram_link'
                'n_followers',
                'n_following',
                'n_likes',
                'n_public_likes',
                'n_pins',
                'n_public_pins',
                'n_boards',
                'n_public_boards',
                'n_unread_notifications',
                'mail_user_follower',
                'mail_board_follower',
                'mail_following_add_pin',
                'mail_following_add_board',
                'mail_repinned',
                'mail_allow_read',
                'mail_following_liked_pin',
                'mail_pin_like',
        )

        read_only_fields = ('pk', 'url', 'n_followers', 'n_following',
            'n_likes' 'n_public_likes', 'n_pins', 'n_public_pins',
            'n_boards', 'n_public_boards', 'n_unread_notifications')
        )


class PublicUserSerializer(UserSerializer):
    """
    A serializer that shows only public field of a user
    All fields read only
    """

    class Meta:
        model = User
        fields = (
                'username',
                'avatar',
                'website',
                'facebook_link',
                'flickr_link',
                'px500_link',
                'twitter_link',
                'gplus_link',
                'pinterest_link',
                'vk_link',
                'instagram_link'
                'n_followers',
                'n_following',
                'n_public_likes',
                'n_public_pins',
                'n_public_boards',
        )

        read_only_fields = fields

