from django.db import models
from django.contrib.auth.models import AbstractUser

from board.slug import unique_slugify



class User(AbstractUser):
    """User extention table."""
    slug = models.SlugField(max_length=30, db_index=True,
                unique=True, verbose_name="Slug")
    avatar = models.ImageField(
            null=True, blank=True,
            upload_to="images/avatars/", 
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
        super(User, self).save()
