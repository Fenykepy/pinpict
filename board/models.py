from django.db import models

from django_extensions.db.fields import UUIDField

from user.models import User


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



class Pin(models.Model):
    """Table for all pins."""
    date_created = models.DateTimeField(auto_now_add=True,
            auto_now=False,
            verbose_name="Creation date")
    date_updated =models.DateTimeField(auto_now_add=True,
            auto_now=True,
            verbose_name="Last update date")
    uniqid = UUIDField(primary_key=True)
    source = models.URLField(verbose_name="Source of web page pin comes from")
    source_file = models.URLField(unique=True,
        verbose_name="Source of original picture")
    n_boards = models.PositiveIntegerField(default=0,
        verbose_name="Board number")
    width = models.PositiveIntegerField(verbose_name="Pin width, in pixels")
    height = models.PositiveIntegerField(verbose_name="Pin height, in pixels")
    size = models.PositiveIntegerField(default=0,
        verbose_name="Size of picture, in bytes")
    type = models.CharField(max_length=30,
        choices=PIN_TYPE_CHOICES, verbose_name="Type of file")



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
    n_pins = models.PositiveIntegerField(default=0, verbose_name="Pins number")
    pins = models.ManyToManyField(Pin, through='Pin_board',
            null=True, blank=True, verbose_name="Pins")
    policy = models.PositiveIntegerField(max_length=150,
                    choices=BOARD_POLICY_CHOICES, verbose_name="Policy")
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['date_created']
        unique_together = ('user', 'slug')



class Pin_board(models.Model):
    """Through table for pins to boards relation,
    add description column."""
    board = models.ForeignKey(Board)
    pin = models.ForeignKey(Pin)
    pin_description = models.TextField(null=True, blank=True,
            verbose_name="Pin description")





