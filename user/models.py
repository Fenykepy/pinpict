import os
import io

from PIL import Image

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import SimpleUploadedFile

from board.slug import unique_slugify
from pinpict.settings import AVATAR_MAX_SIZE, MEDIA_ROOT
from pin.utils import get_sha1_hexdigest


def has_changed(instance, field, manager='objects'):
    """Returns true if a field has changed in a model

    May be used in a model.save() method.

    """
    if not instance.pk:
        return True
    manager = getattr(instance.__class__, manager)
    old = getattr(manager.get(pk=instance.pk), field)
    return not getattr(instance, field) == old



class User(AbstractUser):
    """User extention table."""
    slug = models.SlugField(max_length=30, db_index=True,
                unique=True, verbose_name="Slug")
    uuid = models.CharField(max_length=42, blank=True, null=True)
    uuid_expiration = models.DateTimeField(blank=True, null=True)
    avatar = models.ImageField(
            null=True, blank=True,
            upload_to='images/avatars',
            verbose_name="Avatar",
            help_text="A picture to download as avatar."
    )
    website = models.URLField(
            null=True,
            blank=True,
            verbose_name="Site web",
            help_text="A link to your website."
    )
    facebook_link = models.URLField(
            null=True,
            blank=True,
            verbose_name="Facebook",
            help_text="A link to your facebook page."
    )
    flickr_link = models.URLField(
            null=True,
            blank=True,
            verbose_name="Flickr",
            help_text="A link to your flickr page."
    )
    twitter_link = models.URLField(
            null=True,
            blank=True,
            verbose_name="Twitter",
            help_text="A link to your twitter page."
    )
    gplus_link = models.URLField(
            null=True,
            blank=True,
            verbose_name="Google +",
            help_text="A link to your google + page."
    )
    pinterest_link = models.URLField(
            null=True,
            blank=True,
            verbose_name="Pinterest",
            help_text="A link to your pinterest page."
    )
    vk_link = models.URLField(
            null=True,
            blank=True,
            verbose_name="Vkontakte",
            help_text="A link to your vkontakte page."
    )

    n_public_pins = models.PositiveIntegerField(default=0,
            verbose_name="Public pins'number")
    n_pins = models.PositiveIntegerField(default=0,
            verbose_name="Pins'number")
    n_boards = models.PositiveIntegerField(default=0,
            verbose_name="Boards'number")
    n_public_boards = models.PositiveIntegerField(default=0,
            verbose_name="Public Boards'number")



    def save(self, **kwargs):
        """Make a unique slug from username then save."""
        if self.pk == None:
            slug = '%s' % (self.username)
            unique_slugify(self, slug)


        if self.avatar and has_changed(self, 'avatar'):
            # open Image object
            img = Image.open(self.avatar.file)
            # get Image format
            format = img.format
            # set filename
            filename = '{}.{}'.format(self.id, format.lower())
            # set image size
            size = AVATAR_MAX_SIZE, AVATAR_MAX_SIZE
            # resize
            img.thumbnail(size, Image.ANTIALIAS)
            temp = io.BytesIO()
            img.save(temp, format, optimize=True)
            temp.seek(0)
            uploaded_file = SimpleUploadedFile('temp', temp.read())
            # save avatar
            self.avatar.save(
                    filename,
                    uploaded_file,
                    save=False)

        # save object
        super(User, self).save()
 
            
