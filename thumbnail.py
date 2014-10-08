from wand.image import Image

class ThumbnailFactory(object):
    """Class to create thumbnails from an image file."""

    def __init__(self, filename=None, file=None):
        self.img = None
        self.filename = filename
        self.file = file
        self.ratio = 0.0

        return self._open()

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        """Close file on exit."""
        self.img.close()


    def resize_max(self, max_side):
        # if image is more width than height
        if self.ratio > 1:
            #print('go to resize_width')
            return self.resize_width(max_side)
        # if image is square, or more height than width
        else:
            #print('go to resize_height')
            return self.resize_height(max_side)



    def resize_width(self, target_width):
        # if image is too small, return
        #print('resize_width')
        if self.img.width <= target_width:
            #print('img too small (width)')
            return
        target_height = int(target_width / self.ratio)
        #print('target_width: {}, target_height: {}'.format(target_width, target_height))
        self.img.resize(target_width, target_height)

        return


    def resize_height(self, target_height):
        # if image is too small, return
        #print('resize_height')
        if self.img.height <= target_height:
            #print('img too small (height)')
            return
        target_width = int(target_height * self.ratio)
        #print('target_width: {}, target_height: {}'.format(target_width, target_height))
        self.img.resize(target_width, target_height)

        return


    def resize_crop(self, target_width, target_height):
        # if image is too small, return
        #print('resize_crop')
        if self.img.width <= target_width and self.img.height <= target_height:
            #print('img too small (crop)')

            return

        if self.img.width < target_width:
            #print('width too small')

            return self.resize_height(target_height)

        if self.img.height < target_height:
            #print('height too small')

            return self.resize_width(target_width)

        #print('target_width: {}, target_height: {}'.format(target_width, target_height))
        target_ratio = target_width / target_height

        if self.ratio >= target_ratio:
            self.resize_height(target_height)
            new_width, new_height = self.img.size
            delta = new_width - target_width
            left = int(delta/2)
            upper = 0
            right = left + target_width
            lower = target_height
        else:
            self.resize_width(target_width)
            new_width, new_height = self.img.size
            delta = new_height - target_height
            left = 0
            upper = int(delta/2)
            right = target_width
            lower = upper + target_height

        # crop thumbnail
        self.img.crop(left, upper, right, lower)



    def save(self, filename=None, stream=None, format=None, quality=None):
        if format:
            self.img.format = format
        if quality:
            self.img.compression_quality = quality

        if stream:
            self.img.save(stream)
        elif filename:
            self.img.save(filename=filename)
        else:
            raise

        return


    def _open(self):
        if self.filename:
            #print('open file from filename')
            self.img = Image(filename=self.filename)
        elif self.file:
            #print('open file from stream')
            self.img = Image(file=self.file)
        else:
            raise

        return self._get_ratio()


    def _get_ratio(self):
        self.ratio = self.img.width / self.img.height
        #print('width: {}, height: {}'.format(self.img.width, self.img.height))
        #print('ratio: {}'.format(self.ratio))

        return



