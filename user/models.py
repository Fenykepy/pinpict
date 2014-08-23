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

    def save(self, **kwargs):
        """Make a unique slug from username then save."""
        slug = '%s' % (self.username)
        unique_slugify(self, slug)
        super(User, self).save()
