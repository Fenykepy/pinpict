from django.test import TestCase, Client

from user.models import User
from board.models import Board, Pin, Resource
from board.utils import extract_domain_name

class UtilsTest(TestCase):
    """Utils functions test."""
    def test_extract_domain_name(self):
        urls = [
            {
                'url': 'http://lavilotte-rolle.fr/toto/tata',
                'domain_name': 'lavilotte-rolle.fr',
            },
            {
                'url': 'https://lavilotte-rolle.fr/toto/tata',
                'domain_name': 'lavilotte-rolle.fr',
            },
            {
                'url': 'http://www.lavilotte-rolle.fr',
                'domain_name': 'lavilotte-rolle.fr',
            },
            {
                'url': 'https://www.lavilotte-rolle.fr',
                'domain_name': 'lavilotte-rolle.fr',
            }
        ]

        for elem in urls:
            domain_name = extract_domain_name(elem['url'])
            self.assertEqual(domain_name, elem['domain_name'])



class BoardTest(TestCase):
    """Board app tests."""

    def setUp(self):
        self.user = User.objects.create_user(
                username='flr',
                email='pro@lavilotte-rolle.fr',
                password='top_secret'
        )
        self.user.website = 'http://lavilotte-rolle.fr'
        self.user.save()


        board = Board()
        board.title = 'Paolo Roversi'
        board.description = 'Photographies de Paolo Roversi.'
        board.policy = 1
        board.user = self.user
        board.save()
        

        self.client = Client()



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
           # {
           #     'url': '/board/create/',
           #     'status': 302,
           #     'template': '',
           # },
        ]

        for elem in urls:
            response = self.client.get(elem['url'])
            self.assertEqual(response.status_code, elem['status'])
            response = self.client.get(elem['url'], follow=True)
            self.assertEqual(response.templates[0].name, elem['template'])

    
    def test_board_creation(self):
        """Test new board creation."""
        # login
        login = self.client.login(username='flr', password='top_secret')
        self.assertEqual(login, True)

        # send form
        response = self.client.post('/board/create/', {
            'title': 'Richard Avedon',
            'description': 'Photographies de Richard Avedon',
            'policy': 1,
            }, follow=True
        )
        # assert redirection is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                'board/board_list.html'
        )
        # assert board has been saved in deb
        new_board = Board.objects.get(slug='richard-avedon')
        # assert user is the good one
        self.assertEqual(new_board.user.username, 'flr')


