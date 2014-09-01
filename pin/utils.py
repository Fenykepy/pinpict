import hashlib
import os

from PIL import Image, ImageFile

from pinpict.settings import PREVIEWS_JPG_QUALITY, PREVIEWS_WIDTH, \
        PREVIEWS_CROP, PREVIEWS_ROOT, MEDIA_ROOT


def get_sha1_hexdigest(file):
    """Return sha1 hexadecimal sum of
    given file."""

    sha1 = hashlib.sha1()
    for chunk in file.chunks():
        sha1.update(chunk)

    return sha1.hexdigest()



def extract_domain_name(url):
    """Extract domain name (without www. if any),
    from given url and return it."""

    url = url.lstrip('https://')
    url = url.lstrip('http://')
    url = url.lstrip('www.')

    url_list = url.split('/')

    return url_list[0]



def set_previews_filename(resource):
    """Create a filename from sha1."""
    return '{}.jpg'.format(resource.sha1)



def set_previews_subdirs(resource):
    """Create a path with two subdirectorys from sha1."""
    return '{}/{}/'.format(
        resource.sha1[0:2],
        resource.sha1[2:4]
    )



def save_preview(img, destination):
    """Save a thumbnail.
    img -- Image instance
    destination -- full pathname to output preview
    """
    def save():
        img.save(
                destination,
                "JPEG",
                quality=PREVIEWS_JPG_QUALITY,
                optimize=True,
                progressive=True
        )
    try:
        save()
    except IOError:
        ImageFile.MAXBLOCK = img.size[0] * img.size[1]
        save()



def generate_previews(resource):
    """Create thumbs from resource."""

    filename = set_previews_filename(resource)
    subdirs = set_previews_subdirs(resource)
    resource.previews_path = os.path.join(subdirs, filename)
    resource.save()
    
    for preview in PREVIEWS_WIDTH:
        ## preview[0] -- int width of preview
        ## preview[1] -- string name of subfolder
        # create subdirs if necessary
        dest_path = os.path.join(PREVIEWS_ROOT, preview[1], subdirs)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        # def source name
        source = os.path.join(MEDIA_ROOT, resource.source_file.name)
        # def destination name
        destination = os.path.join(dest_path, filename)
        # create Pil Image instance
        img = Image.open(source)
        full_width, full_height = img.size
        width = preview[0]
        # if image is enought big, create thumbnail
        if full_width > width:
            ratio = full_width / full_height
            height = int(width/ratio)
            size = width, height
            # create preview
            img.thumbnail(size, Image.ANTIALIAS)
            # save preview
            save_preview(img, destination)
        # else, symlink to original file
        else:
            os.symlink(source, destination)














