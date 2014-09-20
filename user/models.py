import os

from PIL import Image

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage

from board.slug import unique_slugify
from pinpict.settings import AVATAR_MAX_SIZE, MEDIA_ROOT
from pin.utils import get_sha1_hexdigest


def set_pathname(instance, filename):
    """Set pathname as <user.id>.<ext>."""
    basename, ext = os.path.splitext(filename)
    # set image name
    name = "{}{}".format(instance.id, ext.lower())
    rel_path = os.path.join('images/avatars', name)

    return rel_path



class User(AbstractUser):
    """User extention table."""
    slug = models.SlugField(max_length=30, db_index=True,
                unique=True, verbose_name="Slug")
    uuid = models.CharField(max_length=42, blank=True, null=True)
    uuid_expiration = models.DateTimeField(blank=True, null=True)
    avatar = models.ImageField(
            null=True, blank=True,
            upload_to=set_pathname,
            verbose_name="Avatar",
            help_text="A picture to download as avatar."
    )
    avatar_sha1 = models.CharField(max_length=42, blank=True, null=True)
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
        resize = False
        if self.pk == None:
            slug = '%s' % (self.username)
            unique_slugify(self, slug)
        if self.avatar and not self.avatar_sha1:
            # it's first avatar upload, compute sha1
            self.avatar_sha1 = get_sha1_hexdigest(self.avatar)
            resize = True
        elif self.avatar:
            sha1 = get_sha1_hexdigest(self.avatar)
            # if it's a new avatar, store new sha1
            if self.avatar_sha1 != sha1:
                resize = True
                self.avatar_sha1 = sha1

        # save object
        super(User, self).save()
        if resize:
            # open Image object
            img = Image.open(self.avatar)
            # get Image format
            format = img.format
            # set image size
            size = AVATAR_MAX_SIZE, AVATAR_MAX_SIZE
            # resize
            img.thumbnail(size, Image.ANTIALIAS)
            try:
                img.save(self.avatar.path, format,
                        quality=90, optimize=True)
            except IOError:
                ImageFile.MAXBLOCK = img.size[0] * img.size[1]
                img.save(self.avatar.path, format,
                        quality=90, optimize=True)

            
