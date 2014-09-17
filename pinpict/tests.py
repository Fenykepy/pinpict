from django.test import TestCase, Client

from user.tests import create_test_users, login, test_urls


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



