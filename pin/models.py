import os

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user.models import User
from board.models import Board
from pin.utils import extract_domain_name, get_sha1_hexdigest



class ResourceFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name):
        return name

    def _save(self, name, content):
        if self.exists(name):
            # if the file exists, do not call the superclasses _save method
            return name
        # if the file is new, DO call it
        return super(ResourceFileSystemStorage, self)._save(name, content)



def set_pathname(instance, filename):
    """Set pathname under form
    full/4a/52/4a523fe9c50a2f0b1dd677ae33ea0ec6e4a4b2a9.ext."""
    sha1 = instance.sha1
    basename, ext = os.path.splitext(filename)
    return os.path.join('previews', 'full', sha1[0:2], sha1[2:4],
            sha1 + ext.lower())



class Resource(models.Model):
    """Table for all ressources."""
    date_created = models.DateTimeField(auto_now_add=True,
            auto_now=False,
            verbose_name="Creation date")
    sha1 = models.CharField(max_length=42, unique=True, db_index=True)
    source_file = models.ImageField(upload_to=set_pathname,
            storage=ResourceFileSystemStorage()
    )
    source_file_url = models.URLField(blank=True, null=True,
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
        verbose_name="Type of file",
        blank=True, null=True)
    order = models.PositiveIntegerField(default=100000)
    previews_path = models.CharField(max_length=254,
        blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True,
            verbose_name="User who originaly uploaded or" +
            " downloaded resource.""")
            

    class Meta:
        ordering = ['order', 'date_created']

    def __str__(self):
        return "%s" % self.source_file



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
    source = models.URLField(null=True, blank=True,
            verbose_name="Web page pin comes from")
    description = models.TextField(verbose_name="Pin description")
    board = models.ForeignKey(Board)
    resource = models.ForeignKey(Resource)
    added_via = models.ForeignKey(User, blank=True, null=True)
    pin_user = models.ForeignKey(User, related_name="pin_user")
    policy = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.description

    def save(self, **kwargs):
        """get domain from source, then save."""
        if self.source:
            self.source_domain = extract_domain_name(self.source)

        super(Pin, self).save()



@receiver(post_save, sender=Pin)
@receiver(post_delete, sender=Pin)
def update_n_pins(sender, instance, **kwargs):
    """Update Board's n_pins, Resource's n_pins and
    User's n_pins after a pin is save or delete."""
    # update board n_pins
    instance.board.n_pins = instance.board.pin_set.all().count()
    instance.board.save()

    # update resource n_pins
    instance.resource.n_pins = instance.resource.pin_set.all().count()
    instance.resource.save()

    # update user n_pins
    n = 0
    for board in instance.board.user.board_set.all():
        n += board.n_pins

    instance.board.user.n_pins = n
    instance.board.user.save()
