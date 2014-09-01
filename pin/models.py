import os

from django.core.files.storage import FileSystemStorage
from django.db import models

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



