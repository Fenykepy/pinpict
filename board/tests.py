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

    def test_urls(self):
        """Test urls and their templates."""
        urls = [
            {
                'url': '/lavilotte-rolle/',
                'status': 200,
                'template': 'board/board_list.html',
            },
        ]

        for elem in urls:
            response = self.client.get(elem['url'])
            self.assertEqual(response.status_code, elem['status'])
            response = self.client.get(elem['url'], follow=True)
            self.assertEqual(response.templates[0].name, elem['template'])
