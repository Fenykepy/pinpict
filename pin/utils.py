import hashlib
import os
import re
import httplib2
import urllib.request

from html.parser import HTMLParser

from PIL import Image, ImageFile

from pinpict.settings import PREVIEWS_WIDTH, PREVIEWS_CROP,\
        PREVIEWS_ROOT, MEDIA_ROOT


ALLOWED_MIME_TYPE = (
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/tiff',
        'image/svg+xml',
)


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



def remove_empty_folders(path):
    # remove empty subfolders
    files = os.listdir(path)
        
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_folders(fullpath)

    # if folder is empty, delete it
    files = os.listdir(path)
    if len(files) == 0:
        os.rmdir(path)



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



class PictureHTMLParser(HTMLParser):
    """Scan for <a> and <img> tags."""
    pictures = []
    url = ''
    root_url = ''
    protocol = ''
    url_path = ''

    IMAGES = ('jpg', 'svg', 'jpeg')

    def url_is_image(self, url):
        extension = url.split('.').pop().lower()
        if extension and extension in self.IMAGES:
            return True
        return False

    def build_absolute_url(self, url):
        # if url starts with 'http', it's absolute
        if url[:4] == 'http':
            return url
        # if url is relative from root, add root_url
        if url[:1] == '/':
            return self.root_url + url
        # if url is relative from current directory, add it to full url
        if url[:1] != '..':
            return self.url + url
        # if url is relative to previous directorys
            # to implement later !!!

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            a = {
                'href': '',
                'alt': '',
            }
            for attr in attrs:
                if attr[0] == 'href':
                    a['href'] = self.build_absolute_url(attr[1])
                if attr[0] == 'title':
                    a['alt'] = attr[1]
            if a['href'] and self.url_is_image(a['href']):
                self.pictures.append(a)

        if tag == 'img':
            img = {
                'href': '',
                'alt': '',
            }
            for attr in attrs:
                if attr[0] == 'src':
                    img['href'] = self.build_absolute_url(attr[1])
                if attr[0] == 'alt':
                    if attr[1] != '':
                        img['alt'] = attr[1]
                if attr[0] == 'title' and img['alt'] == '':
                    img['alt'] = attr[1]
            if img['href'] and self.url_is_image(img['href']):
                self.pictures.append(img)



def scan_html_for_picts(url):
    """Get resource from given url, scan it to find pictures
    (in <img> and <a> tags, return a list of found pictures.
    """
    # get resource from url
    h = httplib2.Http('.cache')
    response, content = h.request(url)
    # return in case of fail
    if response['status'] not in ('200', '304'):
        return []
    # if resource itself is an image return its url
    if response['content-type'][:5] == 'image':
        return [
                {
                    'href': url,
                    'alt': '',
                }
        ]
    charset = re.sub(r".*charset=(?P<charset>\w+)",
            r"\g<charset>", response['content-type'])
    # if charset in known charset… else charset = 'utf-8'
    
    decoded = content.decode(charset)

    split = url.split('//')
    # parse html
    parser = PictureHTMLParser(convert_charrefs=True)
    parser.pictures = []
    parser.url = url
    parser.protocol = split[0] + '//'
    parser.url_path = split[1]
    parser.root_url = parser.protocol + parser.url_path.split('/')[0]
    parser.feed(decoded)
    
    # return pictures list
    return parser.pictures



def get_pict_over_http(url):
    """Retrieve an image over http.
    return False if url is not image
    return temporary path if everything is ok.
    """
    # get file in temp dir
    try:
        local_filename, headers = urllib.request.urlretrieve(url)
    except:
        return False
    # if file is not an image return
    if not headers['Content-Type'] in ALLOWED_MIME_TYPE:
        return False
    # get file extension (because it's used by
    # filestorage rename function)
    extension = headers['Content-Type'][6:]
    if extension == 'jpeg':
        extension = 'jpg'
    # rename temp file with extension
    tmp_name = local_filename + '.' + extension
    os.rename(local_filename, tmp_name)

    return tmp_name






        













