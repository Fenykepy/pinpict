from django.contrib.sitemaps import Sitemap

from user.models import User
from board.models import Board
from pin.models import Pin



class UserSitemap(Sitemap):
    """Site map of all user pages."""
    changefreq = 'weekly'
    priority = 0.1

    def items(self):
        return User.objects.all()

    def lastmod(self, item):
        try:
            last_board = item.board_set.latest('date_updated')
            return last_board.date_updated
        except Board.DoesNotExist:
            return



class BoardSitemap(Sitemap):
    """Site map of all public boards."""
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Board.publics.all()

    def lastmod(self, item):
        return item.date_updated



class PinSitemap(Sitemap):
    """Site map of all public pins."""
    changefreq = 'hourly'
    priority = 1

    def items(self):
        return Pin.objects.filter(policy=1)

    def lastmod(self, item):
        return item.date_updated
