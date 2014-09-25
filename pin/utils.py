import hashlib
import os
import re
import httplib2

from html.parser import HTMLParser

from PIL import Image, ImageFile


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




def save_image(img, destination, type, quality):
    """Save a thumbnail.
    img -- Image instance
    destination -- full pathname to output preview
    type -- image type ('JPEG')
    """
    def save():
        img.save(
                destination,
                type,
                quality=quality,
                optimize=True,
                progressive=True
        )
    try:
        save()
    except IOError:
        ImageFile.MAXBLOCK = img.size[0] * img.size[1]
        save()



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
        # url is href or src element url.
        # self.url is url url comes from.
        # if url starts with 'http', it's absolute
        if url[:4] == 'http':
            return url
        # if url is relative from root, add root_url
        if url[:1] == '/':
            return self.root_url + url
        # if url is relative to current, add url
        if url[:2] == './':
            return self.url + url[2:]
        # if url is relative from current directory, add it to full url
        # if nor '..' nor '/' nor './' it's in current directory
        if url[:2] != '..': 
            return self.url + url
        # if url is relative to previous directorys
        else:
            split = url.split('/')
            parent = 0
            for item in split:
                if item == '..':
                    parent += 1

            list = self.url_path.rstrip('/').split('/')
            if len(list) <= parent:
                # error -> back way is longer than url
                return None
            # troncate list and split, get ['naiet', 'naiena']
            list = list[:-parent]
            split = split[parent:]
            # join list, get 'naiet/naiena'
            url_path = '/'.join(list)
            url_end = '/'.join(split)
            full_url_path = '/'.join([url_path, url_end])
            return self.protocol + full_url_path




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
    parser.protocol = split[0] + '//' # 'http' or 'https'
    parser.url_path = split[1] # everything which follows 'http(s)://'
    parser.root_url = parser.protocol + parser.url_path.split('/')[0]
    parser.feed(decoded)
    
    # return pictures list
    return parser.pictures



