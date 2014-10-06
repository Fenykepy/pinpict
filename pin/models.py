import os
import urllib.request
import imghdr

#from PIL import Image
from wand.image import Image

from django.core.files.storage import FileSystemStorage
from  django.core.files.images import ImageFile
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.http import Http404

from user.models import User
from board.models import Board
from pin.utils import extract_domain_name, save_image, get_sha1_hexdigest
from pinpict.settings import PREVIEWS_WIDTH, PREVIEWS_CROP,\
        PREVIEWS_ROOT, MEDIA_ROOT


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
    return os.path.join(
            'previews',
            'full',
            instance.sha1[0:2],
            instance.sha1[2:4],
            instance.sha1 + '.' + instance.type
    )



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
        verbose_name="Source of original picture", max_length=2000)
    n_pins = models.PositiveIntegerField(default=0,
        verbose_name="Board number")
    width = models.PositiveIntegerField(default=0,
            verbose_name="Pin width, in pixels")
    height = models.PositiveIntegerField(default=0,
            verbose_name="Pin height, in pixels")
    size = models.PositiveIntegerField(default=0,
        verbose_name="Size of picture, in bytes")
    type = models.CharField(max_length=30,
        verbose_name="Type of file")
    previews_path = models.CharField(max_length=254,
        blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True,
            verbose_name="User who originaly uploaded or" +
            " downloaded resource.""")
            

    class Meta:
        ordering = ['date_created']


    def __str__(self):
        return "%s" % self.source_file


    def _set_previews_filename(self):
        """Create preview filename from sha1."""
        return '{}.jpg'.format(self.sha1)


    def _set_previews_subdirs(self):
        """Create preview path with two subdirectorys from sha1."""
        return '{}/{}/'.format(
            self.sha1[0:2],
            self.sha1[2:4]
        )


    def generate_previews(self):
        """Create thumbs from resource."""

        filename = self._set_previews_filename()
        subdirs = self._set_previews_subdirs()
        self.previews_path = os.path.join(subdirs, filename)
        self.save()
        # def source name
        source = os.path.join(MEDIA_ROOT, self.source_file.name)

        def mk_subdirs(size_dir_name):
            """create preview subdirs if they don't exist.
            return full preview pathname"""
            dest_path = os.path.join(PREVIEWS_ROOT, size_dir_name, subdirs)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            # def destination name
            return os.path.join(dest_path, filename)
                

        # generate width based previews
        for preview in PREVIEWS_WIDTH:
            ## preview[0] -- int width of preview
            width = preview[0]
            ## preview[1] -- string name of subfolder
            ## preview[2] -- int JPEG quality
            quality = preview[2]

            # mk subdirs if necessary
            destination = mk_subdirs(preview[1])
            # create Pil Image instance
            img = Image.open(source)
            full_width, full_height = img.size
            # if image is enought big, create thumbnail
            if full_width > width:
                ratio = full_width / full_height
                height = int(width/ratio)
                size = width, height
                # create preview
                img.thumbnail(size, Image.ANTIALIAS)
                # save preview
                save_image(img, destination, "JPEG", quality)
            # else, symlink to original file
            elif not os.path.isfile(destination):
                os.symlink(source, destination)

        # generate width and height based previews
        for preview in PREVIEWS_CROP:
            ## preview[0] -- int width of preview
            width = preview[0]
            ## preview[1] -- int height of preview
            height = preview[1]
            ## preview[2] -- string name of subfolder
            ## preview[3] -- int JPEG quality
            quality = preview[3]

            # create subdirs if necessary
            destination = mk_subdirs(preview[2])
            # create Pil Image instance
            img = Image.open(source)
            full_width, full_height = img.size
            full_ratio = full_width / full_height
            ratio = width / height
            
            # if source is smaller than destination, symlink to original file
            if full_width < width and full_height < height:
                if not os.path.isfile(destination):
                    os.symlink(source, destination)
                continue
           
            # create intermediate thumbnail before crop (much faster)
            # set size (max width, max height) of intermediate thumbnail
            if full_ratio >= ratio:
                size = (int(height * full_ratio + 1), height)
            else:
                size = (width, int(width / full_ratio + 1))
            # create thumbnail
            img.thumbnail(size, Image.ANTIALIAS)
            # get new picture size
            new_width, new_height = img.size
            # define crop coordinates, depending of ratios
            if full_ratio >= ratio:
                delta = new_width - width
                left = int(delta/2)
                upper = 0
                right = left + width
                lower = height
            else:
                delta = new_height - height
                left = 0
                upper = int(delta/2)
                right = width
                lower = upper + height
            
            # crop preview
            img = img.crop((left, upper, right, lower))
            # save preview
            save_image(img, destination, "JPEG", quality)




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
            verbose_name="Web page pin comes from", max_length=2000)
    description = models.TextField(verbose_name="Pin description")
    board = models.ForeignKey(Board)
    resource = models.ForeignKey(Resource)
    added_via = models.ForeignKey(User, blank=True, null=True)
    pin_user = models.ForeignKey(User, related_name="pin_user")
    policy = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.description

    class Meta:
        ordering = ['date_created']

    def save(self, **kwargs):
        """get domain from source, then save."""
        self.policy = self.board.policy
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
    instance.board.user.n_pins = instance.pin_user.get_n_pins()
    instance.board.user.n_public_pins = instance.pin_user.get_n_public_pins()
    instance.board.user.save()




class ResourceFactory(object):
    """Class to create new resources."""
    
    ALLOWED_MIME_TYPE = (
            'image/jpeg',
            'image/png',
            'image/gif',
            'image/tiff',
            'image/svg+xml',
    )
    
    def __init__(self):
        self.resource = None
        self.path = None
        self.filepath = None
        self.sha1 = None
        return


    def make_resource_from_url(self, url, user=None):
        """Make a resource from given url.
        It must point to an image content-type file.
        return resource object
        """
        # set up
        self.resource = Resource()
        self.resource.source_file_url = url[:2000]
        self.resource.user = user
        # get file from http
        return self._get_file_over_http(url)


    def make_resource_from_file(self, file, user=None):
        """Make a resource from given file.
        It must be an image file.
        """
        # set up
        self.resource = Resource()
        self.resource.user = user
        if not os.path.isfile(file):
            raise Http404
        self.filepath = file

        return self._get_file_sha1(file)
        

    
    def make_tmp_resource(self, file):
        """Store given file in temporary folder if
        no resource exists with its hash, return filepath
        if resource exists with its hash, remove file and return resourceo        file -- in memory uploaded file object.
        """
        # return resource object if any, else self.filepath, which is None
        resource = self._get_file_sha1(file)
        if resource:
            return resource

        # set pathname as MEDIA_ROOT/tmp/<sha1>
        pathname = os.path.join(
                self._get_tmp_resource_path(),
                self.sha1
        )

        # save file in tmp folder
        with open(pathname, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        del file

        # return file url relative to MEDIA_URL
        return 'tmp/' + self.sha1



    def _get_file_over_http(self, url):
        """Retrieve a image file over http.
        return False if file is not an image.
        return file path otherwise.
        """
        # get file in tmp dir
        #try:
        print(url)
        self.filepath, headers = urllib.request.urlretrieve(url)
        #except:
        #    print('error with urllib')
        #    return False
        # if file is not an image, return false
        if not headers['Content-Type'].lower() in self.ALLOWED_MIME_TYPE:
            print('file is not image type')
            print(headers['Content-Type'])
            return False
        # else return file_path
        return self._get_file_sha1(self.filepath)

    
    def _get_file_sha1(self, file):
        """Return file sha1 hash."""
        try:
            self.sha1 = get_sha1_hexdigest(file)
        except AttributeError:
            with open(file, 'rb') as f:
                self.sha1 = get_sha1_hexdigest(ImageFile(f))
        if self.resource:
            self.resource.sha1 = self.sha1
        return self._get_clone(self.sha1)


    def _get_clone(self, sha1):
        """Search existing resource with same hash.
        if any returns it, else return false.
        """
        try:
            clone = Resource.objects.get(sha1=sha1)
        except:
            return self._create_new_resource()
        print('clone')
        return clone


    def _get_image_type(self):
        """Return image type of self.filepath."""
        with Image(filename=self.filepath) as img:
            type = img.format
        # in case of no result, try other way
        if not type:
            print('type: {}'.format(type))
            type = imghdr.what(self.filepath)
        # last solution, take actual extension
        if not type:
            print('type: {}'.format(type))
            basename, ext = os.path.splitext(self.filepath)
            type = ext.strip('.')
        # else use default unknown ext
        if not type:
            print('type: {}'.format(type))
            type = 'unknown'

        return type.lower()


    def _get_tmp_resource_path(self):
        """Return path tmp file will be saved to."""
        self.path = os.path.join(MEDIA_ROOT, 'tmp')
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        return self.path



    def _create_new_resource(self):
        """Create a new resource."""
        if not self.resource:
            # tmp resource creation, return self.filepath
            return self.filepath
        # create type before opening file
        type = self._get_image_type()
        print(type)
        with open(self.filepath, 'rb') as f:
            file = ImageFile(f)
            self.resource.source_file = file
            self.resource.size = file.size
            self.resource.width = file.width
            self.resource.height = file.height
            self.resource.type = type
            self.resource.save()
            self.resource.generate_previews()


        return self.resource

            

       
 
