import hashlib
import os

from PIL import Image, ImageFile

from pinpict.settings import PREVIEWS_WIDTH, PREVIEWS_CROP,\
        PREVIEWS_ROOT, MEDIA_ROOT


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



def save_preview(img, destination, quality):
    """Save a thumbnail.
    img -- Image instance
    destination -- full pathname to output preview
    """
    def save():
        img.save(
                destination,
                "JPEG",
                quality=quality,
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
    # def source name
    source = os.path.join(MEDIA_ROOT, resource.source_file.name)

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
            save_preview(img, destination, quality)
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
        save_preview(img, destination, quality)



















