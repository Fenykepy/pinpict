from django.db import models

from django_extensions.db.fields import UUIDField
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User
from board.slug import unique_slugify
from board.utils import extract_domain_name

BOARD_POLICY_CHOICES = (
            (0, 'Private'),
            (1, 'Public'),
        )


PIN_TYPE_CHOICES = (
        ('jpg', 'jpg'),
        ('tiff', 'tiff'),
        ('png', 'png'),
        ('gif', 'gif'),
        ('svg', 'svg'),
)



class PublicBoardsManager(models.Manager):
    """Returns a queryset with all public boards."""
    def get_query_set(self):
        return super(PublicBoardsManager, self).get_query_set().filter(
                policy=1)




class PrivateBoardsManager(models.Manager):
    """Returns a queryset with all public boards."""
    def get_query_set(self):
        return super(PrivateBoardsManager, self).get_query_set().filter(
                policy=0)



class Board(models.Model):
    """Table for all boards."""
    date_created = models.DateTimeField(auto_now_add=True,
            auto_now=False,
            verbose_name="Creation date")
    date_updated =models.DateTimeField(auto_now_add=True,
            auto_now=True,
            verbose_name="Last update date")
    title = models.CharField(max_length=254, verbose_name="Title")
    slug = models.SlugField(max_length=254, db_index=True,
            verbose_name="Slug")
    description = models.TextField(null=True, blank=True,
            verbose_name="Board description")
    n_pins = models.PositiveIntegerField(default=0,
            verbose_name="Pins number")
    policy = models.PositiveIntegerField(
            choices=BOARD_POLICY_CHOICES, verbose_name="Policy")
    user = models.ForeignKey(User)
    order = models.PositiveIntegerField(default=100000)

    # managers
    objects = models.Manager()
    publics = PublicBoardsManager()
    privates = PrivateBoardsManager()

    class Meta:
        ordering = ['order', 'date_created']
        unique_together = (('user', 'slug'),)

    def save(self, **kwargs):
        """Make a unique slug for from title, then save."""
        slug = '%s' % (self.title)
        unique_slugify(self, slug,
                queryset=Board.objects.filter(user=self.user))
        super(Board, self).save()

    def __str__(self):
        return "%s" % self.title



class Resource(models.Model):
    """Table for all ressources."""
    date_created = models.DateTimeField(auto_now_add=True,
            auto_now=False,
            verbose_name="Creation date")
    uniqid = UUIDField(unique=True, db_index=True)
    pathname = models.CharField(max_length=254, blank=True, null=True,
        verbose_name="Pathname to file, including last directory " +
        "and extension")
    source_file = models.URLField(unique=True,
        verbose_name="Source of original picture")
    n_pins = models.PositiveIntegerField(default=0,
        verbose_name="Board number")
    width = models.PositiveIntegerField(default=0,
            verbose_name="Pin width, in pixels")
    height = models.PositiveIntegerField(default=0,
            verbose_name="Pin height, in pixels")
    size = models.PositiveIntegerField(default=0,
        verbose_name="Size of picture, in bytes")
    type = models.CharField(max_length=30,
        choices=PIN_TYPE_CHOICES, verbose_name="Type of file")

    def __str__(self):
        return "%s" % self.uniqid



@receiver(post_save, sender=Resource)
def set_pathname(sender, instance, **kwargs):
    """Complete pathname from uniqid then save."""
    if not instance.pathname:
        instance.pathname = "{0}/{1}.{2}".format(
                instance.uniqid[:2],
                instance.uniqid,
                instance.type
            )
        instance.save()



class Pin(models.Model):
    """Table for all pins."""
    date_created = models.DateTimeField(auto_now_add=True,
            auto_now=False,
            verbose_name="Creation date")
    date_updated =models.DateTimeField(auto_now_add=True,
            auto_now=True,
            verbose_name="Last update date")
    source_domain = models.CharField(max_length=254, blank=True, null=True,
            verbose_name="Domain pin comes from")
    source = models.URLField(verbose_name="Web page pin comes from")
    description = models.TextField(verbose_name="Pin description")
    board = models.ForeignKey(Board)
    resource = models.ForeignKey(Resource)

    def __str__(self):
        return "%s" % self.description

    def save(self, **kwargs):
        """get domain from source, then save."""
        self.source_domain = extract_domain_name(self.source)

        super(Pin, self).save()






