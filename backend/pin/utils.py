import hashlib
import os
import re

from html.parser import HTMLParser


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



class PictureHTMLParser(HTMLParser):
    """Scan for <a> and <img> tags."""
    IMAGES = ('jpg', 'svg', 'jpeg')

    def __init__(self, url=None, *args, **kwargs):
        super(PictureHTMLParser, self).__init__(*args, **kwargs)
        if not url:
            return False
        self.url = url
        split = url.split('//')
        self.protocol = split[0] + '//' # 'http' or 'https'
        self.url_path = split[1] # everything which follows 'http(s)://'
        self.root_url = self.protocol + self.url_path.split('/')[0]
        self.pictures = []
        self.urls = set()


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
                return False
            # troncate list and split, get ['naiet', 'naiena']
            list = list[:-parent]
            split = split[parent:]
            # join list, get 'naiet/naiena'
            url_path = '/'.join(list)
            url_end = '/'.join(split)
            full_url_path = '/'.join([url_path, url_end])
            return self.protocol + full_url_path




    def handle_starttag(self, tag, attrs):
        """ Store url and description in a tuple as:
            (url, description)
            img tags goes to self.img list
            a tags goes to self.a list.
        """
        if tag == 'a' or tag == 'img':
            src = ''
            alt = ''
            title = ''
            for attr in attrs:
                # get url
                if attr[0] == 'href' or attr[0] == 'src':
                    src = self.build_absolute_url(attr[1])

                # get description (title or alt, with priority for alt)
                if attr[0] == 'alt' and attr[1]:
                    alt = attr[1]
                if not alt and attr[0] == 'title' and attr[1]:
                    title = attr[1]
            # if src isn't an image return, or src is already in set
            if not src or src in self.urls:
                return
            # if it's <a> tag and src hasn't image extension, return
            if tag == 'a' and not self.url_is_image(src):
                return
            pict = {
                'href': src,
                'alt': '',
            }
            # if we got an alt attribute, use it
            if alt:
                pict['alt'] = alt
            # if we got a title attribute, use it
            elif title:
                pict['alt'] = title
            # add pict to pictures list and set
            self.urls.add(src)
            self.pictures.append(pict)




