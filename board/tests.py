from django.test import TestCase, Client

from user.models import User
from board.models import Board, Pin, Pin_board

class BoardTest(TestCase):
    """Board app tests."""

    def setUp(self):
        self.user = User.objects.create_user(
                username='lavilotte-rolle',
                email='pro@lavilotte-rolle.fr',
                password='top_secret'
        )
        self.user.website = 'http://lavilotte-rolle.fr'
        self.user.save()

        self.client = Client()

    def test_fixtures(self):
        """Test that fixtures are correctly set up."""
        # get boards owner
        user = User.objects.get(slug='flr')
        # get boards
        boards = Board.objects.filter(user=user)
        # chekw boards
        self.assertEqual(boards[0].title, 'Paolo Roversi')
        self.assertEqual(boards[0].slug, 'paolo-roversi')
        self.assertEqual(boards[0].description,
                'Photographies de Paolo Roversi')
        self.assertEqual(boards[0].policy, 1)
        date = False
        update = False
        if boards[0].date_created:
            date = True
        if boards[1].date_updated:
            update = True
        self.assertEqual(date, True)
        self.assertEqual(update, True)

    def test_urls(self):
        """Test urls and their templates."""
        urls = [
            {
                'url': '/flr/',
                'status': 200,
                'template': 'board/board_list.html',
            },
            {
                'url': '/flr/paolo-roversi/',
                'status': 200,
                'template': 'board/pin_list.html',
            },
        ]

        for elem in urls:
            response = self.client.get(elem['url'])
            self.assertEqual(response.status_code, elem['status'])
            response = self.client.get(elem['url'], follow=True)
            self.assertEqual(response.templates[0].name, elem['template'])
