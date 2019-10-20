from PIL import Image

class ThumbnailFactory(object):
    """Class to create thumbnails from a image file."""


    def __init__(self, filename=None):
        self.img = None
        self.filename = filename
        self.ratio = 0.0
        
        return self._open()


    def __enter__(self, *args):
        return self


    def __exit__(self, *args):
        """Close file on exit"""
        print('close and exit')
        self.img.close()


    def _open(self):
        print('open {}'.format(self.filename))
        self.img = Image.open(self.filename)

        return self._get_ratio()


    def _get_ratio(self):
        self.ratio = self.img.width / self.img.height
        print('set ratio {}'.format(self.ratio))
        return


    def save(self, filename, quality=70):
        print('save image')
        print('image size {}'.format(self.img.size))
        self.img.save(
            filename,
            'jpeg',
            quality = quality,
            progressive = True,
        )
        print('image saved as {}'.format(filename))

        return


    def resize_max(self, max_side):
        print('resize max')
        # if image is landscape oriented
        if self.ratio > 1:
            print('ratio > 1, resize_width')
            return self.resize_width(max_side)
        else:
            print('ratio <= 1, resize_height')
            return self.resize_height(max_side)


    def resize_width(self, target_width):
        print('resize_width')
        # if image is too small, do nothing
        if self.img.width <= target_width:
            print('image too small, return')
            return

        target_height = int(target_width / self.ratio)
        print('target_width: {}, target_height: {}'.format(target_width, target_height))
        self.img = self.img.resize((target_width, target_height))
        print('image size {}'.format(self.img.size))
        
        return


    def resize_height(self, target_height):
        print('resize_height')
        # if image is too small, do nothing
        if self.img.height <= target_height:
            print('image too small, return')
            return

        target_width = int(target_height * self.ratio)
        print('target_width: {}, target_height: {}'.format(target_width, target_height))
        self.img = self.img.resize((target_width, target_height))

        return


    def resize_crop(self, target_width, target_height):
        print('resize_crop')
        # if image is too small, do nothing
        if self.img.width <= target_width and self.img.height <= target.height:
            print('image too small, return')
            return

        if self.img.width < target_width:
            print('width too small, resize_height')
            return self.resize_height(target_height)

        if self.img.height < target_height:
            print('height too small, resize_width')
            return self.resize_width(target_width)

        target_ratio = target_width / target_height

        if self.ratio >= target_ratio:
            self.resize_height(target_height)
            new_width, new_height = self.img.size
            delta = new_width - target_width
            left = int(delta / 2)
            upper = 0
            right = left + target_width
            lower = target_height
        else:
            self.resize_width(target_width)
            new_width, new_height = self.img.size
            delta = new_height - target_height
            left = 0
            upper = int(delta / 2)
            right = target_width
            lower = upper + target_height

        # crop thumbnail
        self.img = self.img.crop((left, upper, right, lower))

        return





