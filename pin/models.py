import os
from django.db import models
from django.db.models.signals import post_delete
from django.core.files.storage import FileSystemStorage
from django.dispatch import receiver

from PIL import Image

from user.models import User
from board.models import Board
from pin.utils import extract_domain_name, get_sha1_hexdigest

# to refactore
from pinpict.settings import PREVIEWS_WIDTH, PREVIEWS_CROP,\
        PREVIEWS_ROOT, MEDIA_ROOT
from thumbnail import ThumbnailFactory

# to delete after migration
import imghdr
from uuid import uuid4
from django.core.files.images import ImageFile
from django.http import Http404
from django.utils.encoding import iri_to_uri


# we keep resourceFileSystemStorage until existing db has been migrated
class ResourceFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        return name

    def _save(self, name, content):
        if self.exists(name):
            # if the file exists, do not call the superclasses _save method
            return name
        # if the file is new, DO call it
        return super(ResourceFileSystemStorage, self)._save(name, content)



class PinFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        return name

    def _save(self, name, content):
        if self.exists(name):
            # if the file exists, do not call the superclasses _save method
            return name
        # if the file is new, DO call it
        return super(PinFileSystemStorage, self)._save(name, content)


def set_subdirs(instance, dir):
    """Set subdirs under form <dir>/4a/52/"""
    return os.path.join(
            dir,
            instance.sha1[0:2],
            instance.sha1[2:4]
    )


def mk_subdirs(instance, dir):
    """Make subdirs if necessary."""
    path = os.path.join(
            PREVIEWS_ROOT,
            set_subdirs(instance, dir)
    )
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def set_pathname(instance, filename):
    """Set pathname under form
    previews/full/4a/52/4a523fe9c50a2f0b1dd677ae33ea0ec6e4a4b2a9
    """
    return os.path.join(
            'previews',
            set_subdirs(instance, 'full'),
            instance.sha1
    )



class Pin(models.Model):
    """Table for all pins."""
    sha1 = models.CharField(max_length=42, db_index=True, null=True)
    source_file = models.ImageField(upload_to=set_pathname,
            storage=PinFileSystemStorage(),
            null=True,
    )
    source_file_url = models.URLField(blank=True, null=True,
        verbose_name="Source of original picture", max_length=2000)
    source_domain = models.CharField(max_length=254, blank=True, null=True,
            verbose_name="Domain pin comes from")
    source = models.URLField(null=True, blank=True,
            verbose_name="Web page pin comes from", max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True,
            verbose_name="Creation date")
    date_updated =models.DateTimeField(auto_now=True,
            verbose_name="Last update date")
    description = models.TextField(verbose_name="Pin description")
    board = models.ForeignKey(Board,
            related_name="pins", on_delete=models.CASCADE)
    added_via = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pin_user")
    policy = models.PositiveIntegerField(blank=True, null=True)
    owner_rate = models.PositiveSmallIntegerField(default=0, verbose_name="Rate")
    likes = models.ManyToManyField(User, blank=True,
            related_name="likes")
    n_likes = models.PositiveIntegerField(default=0, verbose_name="Number of likes")

    class Meta:
        ordering = ['date_created']


    def __str__(self):
        return "%s" % self.description


    def increase_n_pins(self):
        """Increase number of pins after pin creation."""
        # increase board n_pins
        self.board.n_pins += 1
        self.board.save()

        # increase user n_pins
        self.user.n_pins += 1
        if self.board.policy == 1:
            self.user.n_public_pins += 1
        self.user.save()


    def set_n_likes(self):
        """set number of likes."""
        self.n_likes = self.likes.all().count()
        self.save()


    def generate_previews(self):
        """Create thumbnails from pin."""
        
        # generate width based previews
        for preview in PREVIEWS_WIDTH:
            target_width = preview[0]
            dir = preview[1]
            quality = preview[2]
            destination = os.path.join(mk_subdirs(self, dir), self.sha1)

            with ThumbnailFactory(filename=self.source_file) as img:
                img.resize_width(target_width)
                img.save(destination, quality=quality)



        # generate width and height based previews
        for preview in PREVIEWS_CROP:
            target_width = preview[0]
            target_height = preview[1]
            dir = preview[2]
            quality = preview[3]
            destination = os.path.join(mk_subdirs(self, dir), self.sha1)
 
            with ThumbnailFactory(filename=self.source_file) as img:
                img.resize_crop(target_width, target_height)
                img.save(destination, quality=quality)


           

    def save(self, **kwargs):
        """get domain from source, then save."""

        self.policy = self.board.policy
        if self.source:
            self.source_domain = extract_domain_name(self.source)

        # compute sha1 here
        self.sha1 = get_sha1_hexdigest(self.source_file)

        # if created 
        if not self.pk:
            # increase pins number
            self.increase_n_pins()
            # set board covers
            self.board.set_covers()
        # else check if board has changed
        else:
            old = Pin.objects.get(pk=self.pk)
            if old.board != self.board:
                # decrease old board pins number
                old.board.n_pins -= 1
                old.board.save()
                # increase new board pins number
                self.board.n_pins += 1
                self.board.save()
                # update user's publics pins number
                self.pin_user.n_public_pins = self.pin_user.get_n_public_pins()
                self.pin_user.save()
                # set old and new board covers
                old.board.set_covers()
                self.board.set_covers()

        
        super(Pin, self).save()

        # generate previews
        self.generate_previews()

        # parse and add tags here
        hashtags = extract_hashtags(self.description)
        for hashtag in hashtags:
            tag, created = Tag.objects.get_or_create(name=hashtag)
            tag.pins.add(self)



class Tag(models.Model):
    """Table for all tags."""
    name=models.CharField(primary_key=True, max_length=254)
    pins = models.ManyToManyField(Pin, blank=True)



def extract_hashtags(s):
    return set(part[1:] for part in s.split() if part.startswith('#'))



@receiver(post_delete, sender=Pin)
def decrease_n_pins(sender, instance, **kwargs):
    """Decrease number of pins after a pin deletion."""
    # decrease board n_pins
    instance.board.n_pins -= 1
    instance.board.save()

    # decrease user n_pins
    instance.pin_user.n_pins -= 1
    if instance.board.policy == 1:
        instance.pin_user.n_public_pins -= 1
    instance.pin_user.save()

    # decrease resource n_pins
    instance.resource.n_pins -= 1
    instance.resource.save()

    # set board covers
    instance.board.set_covers()






