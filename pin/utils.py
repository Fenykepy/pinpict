import hashlib
import os
import re
import httplib2

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



def scan_html_for_picts(url):
    """Get resource from given url, scan it to find pictures
    (in <img> and <a> tags, return a list of found pictures.
    """

    PYTHON_CODEC = (
            # codec   # aliases
            'ascii', '646', 'us-ascii',
            'big5', 'big5-tw', 'csbig5',
            'big5hkscs', 'big5-hkscs', 'hkscs',
            'cp037', 'IBM037', 'IBM039',
            'cp273', '273', 'IBM273', 'csIBM273',
            'cp424', 'EBCDIC-CP-HE', 'IBM424',
            'cp437', '437', 'IBM437',
            'cp500', 'EBCDIC-CP-BE', 'EBCDIC-CP-CH', 'IBM500',
            'cp720',
            'cp737',
            'cp775', 'IBM775',
            'cp850', '850', 'IBM850',
            'cp852', '852', 'IBM852',
            'cp855', '855', 'IBM855',
            'cp856',
            'cp857', '857', 'IBM857',
            'cp858', '858', 'IBM858',
            'cp860', '860', 'IBM860',
            'cp861', '861', 'CP-IS', 'IBM861',
            'cp862', '862', 'IBM862',
            'cp863', '863', 'IBM863',
            'cp864', 'IBM864',
            'cp865', '865', 'IBM865',
            'cp866', '866', 'IBM866',
            'cp869', '869', 'CP-GR', 'IBM869',
            'cp874',
            'cp875',
            'cp932', '932', 'ms932', 'mskanji', 'ms-kanji',
            'cp949', '949', 'ms949', 'uhc',
            'cp950', '950', 'ms950',
            'cp1006',
            'cp1026', 'ibm1026',
            'cp1125', '1125', 'ibm1125', 'cp866u', 'ruscii',
            'cp1140', 'ibm1140',
            'cp1250', 'windows-1250',
            'cp1251', 'windows-1251',
            'cp1252', 'windows-1252',
            'cp1253', 'windows-1253',
            'cp1254', 'windows-1254',
            'cp1255', 'windows-1255',
            'cp1256', 'windows-1256',
            'cp1257', 'windows-1257',
            'cp1258', 'windows-1258',
            'jp', 'eucjp', 'ujis', 'u-jis',
            'euc_jis_2004', 'jisx0213', 'eucjis2004',
            'euc_jisx0213', 'eucjisx0213',
            'euc_kr', 'euckr', 'korean', 'ksc5601', 'ks_c-5601',
                'ks_c-5601-1987', 'ksx1001', 'ks_x-1001',
            'gb2312', 'chinese', 'csiso58gb231280', 'euc- cn', 
                'euccn', 'eucgb2312-cn', 'gb2312-1980', 'gb2312-80', 'iso- ir-58',
            'gbk 936', 'cp936', 'ms936',
            'gb18030', 'gb18030-2000',
            'hz', 'hzgb', 'hz-gb', 'hz-gb-2312',
            'iso2022_jp', 'csiso2022jp', 'iso2022jp', 'iso-2022-jp',
            'iso2022_jp_1', 'iso2022jp-1', 'iso-2022-jp-1',
            'iso2022_jp_2', 'iso2022jp-2', 'iso-2022-jp-2',
            'iso2022_jp_2004', 'iso2022jp-2004', 'iso-2022-jp-2004',
            'iso2022_jp_3', 'iso2022jp-3', 'iso-2022-jp-3',
            'iso2022_jp_ext', 'iso2022jp-ext', 'iso-2022-jp-ext',
            'iso2022_kr', 'csiso2022kr', 'iso2022kr', 'iso-2022-kr',
            'latin_1 iso-8859-1', 'iso8859-1', '8859', 'cp819', 'latin', 'latin1', 'L1',
            'iso8859_2', 'iso-8859-2', 'latin2', 'L2',
            'iso8859_3', 'iso-8859-3', 'latin3', 'L3',
            'iso8859_4', 'iso-8859-4', 'latin4', 'L4',
            'iso8859_5', 'iso-8859-5', 'cyrillic',
            'iso8859_6', 'iso-8859-6', 'arabic',
            'iso8859_7', 'iso-8859-7', 'greek', 'greek8',
            'iso8859_8', 'iso-8859-8', 'hebrew',
            'iso8859_9', 'iso-8859-9', 'latin5', 'L5',
            'iso8859_10', 'iso-8859-10', 'latin6', 'L6',
            'iso8859_13', 'iso-8859-13', 'latin7', 'L7',
            'iso8859_14', 'iso-8859-14', 'latin8', 'L8',
            'iso8859_15', 'iso-8859-15', 'latin9', 'L9',
            'iso8859_16', 'iso-8859-16', 'latin10', 'L10',
            'johab', 'cp1361', 'ms1361',
            'koi8_r',
            'koi8_u',
            'mac_cyrillic', 'maccyrillic',
            'mac_greek', 'macgreek',
            'mac_iceland', 'maciceland',
            'mac_latin2', 'maclatin2', 'maccentraleurope',
            'mac_roman', 'macroman', 'macintosh',
            'mac_turkish', 'macturkish',
            'ptcp154', 'csptcp154', 'pt154', 'cp154', 'cyrillic-asian',
            'shift_jis', 'csshiftjis', 'shiftjis', 'sjis', 's_jis',
            'shift_jis_2004', 'shiftjis2004', 'sjis_2004', 'sjis2004',
            'shift_jisx0213', 'shiftjisx0213', 'sjisx0213', 's_jisx0213',
            'utf_32', 'U32', 'utf32',
            'utf_32_be', 'UTF-32BE',
            'utf_32_le', 'UTF-32LE',
            'utf_16', 'U16', 'utf16',
            'utf_16_be', 'UTF-16BE',
            'utf_16_le', 'UTF-16LE',
            'utf_7', 'U7', 'unicode-1-1-utf-7',
            'utf_8', 'U8', 'UTF', 'utf8',
            'utf_8_sig',
    )

    # get resource from url
    h = httplib2.Http('.cache')
    #print('url used in html parser: {}'.format(url))
    response, content = h.request(url, headers={
            'User-agent': 'Mozilla/5.0'})

    # return in case of fail
    if not response.status in (200, 304, 302):
        print('error {}'.format(response.status))
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
    if not charset in PYTHON_CODEC:
        #print('extracted charset:')
        #print(charset)
        #print('response content-type:')
        #print(response['content-type'])
        #print('wrong charset, use utf-8')
        #for elem in response:
            #print('{}: {}'.format(elem, response[elem]))

        charset = 'utf-8'
    
    decoded = content.decode(charset, errors='replace')
    print(decoded)

    # parse html
    parser = PictureHTMLParser(convert_charrefs=True, url=url)
    parser.feed(decoded)

    print(parser.pictures)
    
    
    # return pictures list
    return parser.pictures




