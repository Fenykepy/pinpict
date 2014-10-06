from wand.image import Image

class ThumbnailFactory(object):
    """Class to create thumbnails from an image file."""

    def __init__(self, filename=None, file=None):
        self.img = None
        self.filename = filename
        self.file = file
        self.ratio = 0.0

        return self._open()


    def resize_max(self, max_side):
        # if image is more width than height
        if self.ratio > 1:
            print('go to resize_width')
            return self.resize_width(max_side)
        # if image is square, or more height than width
        else:
            print('go to resize_height')
            return self.resize_height(max_side)



    def resize_width(self, target_width):
        # if image is too small, return
        print('resize_width')
        if self.img.width <= target_width:
            print('img too small')
            return
        target_height = int(target_width / self.ratio)
        print('target_width: {}, target_height: {}'.format(target_width, target_height))
        self.img.resize(target_width, target_height)

        return


    def resize_height(self, target_height):
        # if image is too small, return
        print('resize_height')
        if self.img.height <= target_height:
            print('img too small')
            return
        target_width = int(target_height * self.ratio)
        print('target_width: {}, target_height: {}'.format(target_width, target_height))
        self.img.resize(target_width, target_height)

        return


    def resize_crop(self, target_width, target_height):
        # if image is too small, return
        print('resize_crop')
        if self.img.width <= target_width and self.img.height <= target_side:
            print('img too small')
            return
        print('target_width: {}, target_height: {}'.format(target_width, target_height))


    def save_as_stream(self, stream):
        self.img.save(stream)
        self.img.close()

        return


    def save_as_file(self, filename):
        self.img.save(filename=filename)
        self.img.close()

        return


    def _open(self):
        if self.filename:
            print('open file from filename')
            self.img = Image(filename=self.filename)
        elif self.file:
            print('open file from stream')
            self.img = Image(file=self.file)
        else:
            raise Error

        return self._get_ratio()


    def _get_ratio(self):
        self.ratio = self.img.width / self.img.height
        print('width: {}, height: {}'.format(self.img.width, self.img.height))
        print('ratio: {}'.format(self.ratio))

        return



