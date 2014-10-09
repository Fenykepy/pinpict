from django.test import TestCase, Client

from user.tests import create_test_users, login, test_urls
from board.tests import create_test_boards, create_test_private_boards
from pin.tests import create_test_resources, create_test_pins, \
        create_test_private_pins

class HomePageTest(TestCase):
    """Home Page test."""

    def setUp(self):
        # create users
        create_test_users(self)
        # start client
        self.client = Client()


    def test_urls(self):
        urls = [
            # should redirect to login page
            {
                'url': '/',
                'status': 302,
                'template': 'user/user_login.html',
            },
        ]
        test_urls(self, urls)



    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)
        urls = [
            # should redirect to user page
            {
                'url': '/',
                'status': 302,
                'template': 'board/board_list.html',
            },
        ]
        test_urls(self, urls)


class SitemapTest(TestCase):
    """Site map test."""

    def setUp(self):
        # create users
        create_test_users(self)
        # create boards
        create_test_boards(self)
        # create private boards
        create_test_private_boards(self)
        # create resources
        create_test_resources(self)
        # create pins
        create_test_pins(self)
        # create private pins
        create_test_private_pins(self)
        # launch client
        self.client = Client()


    def test_sitemaps(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        # 2 users, 2 public pins and 2 public boards
        self.assertEqual(len(response.context['urlset']), 6)



