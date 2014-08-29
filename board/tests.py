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
            # to reactivate when login page will work
           # {
           #     'url': '/board/create/',
           #     'status': 302,
           #     'template': 'board/board_forms.html',
           # },
           #{
           #    'url': '/flr/paolo-roversi/edit/',
           #    'status': 302,
           #    'template': 'board/board_forms.html',
           #},
           #{
           #    'url': '/flr/paolo-roversi/delete/',
           #    'status': 302,
           #    'template': 'board/board_delete.html',
            #},
            
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
        # assert board has been saved in db
        new_board = Board.objects.get(slug='richard-avedon')
        # assert user is the good one
        self.assertEqual(new_board.user.username, 'flr')



    def test_board_update(self):
        """Test board update."""
        # login
        login = self.client.login(username='flr', password='top_secret')
        self.assertEqual(login, True)

        # send form
        response = self.client.post('/flr/paolo-roversi/edit/', {
            'title': 'Paolo Roversi',
            'description': 'Photographies de Paolo Roversi :)',
            'policy': 1,
            }, follow=True
        )

        # assert redirection is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                'board/board_list.html'
        )
        # assert board has been saved in db
        new_board = Board.objects.get(slug='paolo-roversi')
        # assert description is new one
        self.assertEqual(new_board.description, 'Photographies de Paolo Roversi :)')


    def test_board_update_with_wrong_user(self):
        """Test board update with a user which is not owner of board."""

        self.user2 = User.objects.create_user(
                username='toto',
                email='toto@lavilotte-rolle.fr',
                password='top_secret'
        )

        # login with user 2
        login = self.client.login(username='toto', password='top_secret')
        self.assertEqual(login, True)
        
        # get form
        response = self.client.get('/flr/palo-roversi/edit/')
        # assert user has been redirected to home page
        self.assertEqual(response.status_code, 404)
        # get form and follow redirection
        response = self.client.get('/flr/palo-roversi/edit/', follow=True)
        self.assertEqual(response.templates[0].name,
                '404.html'
        )

        # try to send form
        response = self.client.post('/flr/paolo-roversi/edit/', {
            'title': 'Paolo Roversi',
            'description': "Je n'ai pas à éditer ce tableau",
            'policy': 1,
            },
        )
        # assert user has been redirected to home page
        self.assertEqual(response.status_code, 404)

        # try to submit form and follow redirection
        response = self.client.post('/flr/paolo-roversi/edit/', {
            'title': 'Paolo Roversi',
            'description': "Je n'ai pas à éditer ce tableau",
            'policy': 1,
            }, follow=True,
        )
        self.assertEqual(response.templates[0].name,
                '404.html'
        )

        # assert changes haven't been save in db
        new_board = Board.objects.get(slug='paolo-roversi')
        # assert description is new one
        self.assertEqual(new_board.description, 'Photographies de Paolo Roversi.')

    

    def test_board_delete(self):
        """Test board deletion."""
        # login
        login = self.client.login(username='flr', password='top_secret')
        self.assertEqual(login, True)

        # send form
        response = self.client.post('/flr/paolo-roversi/delete/',
                follow=True
        )

        # assert redirection is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                'board/board_list.html'
        )
        # assert board has been deleted from db
        old_board = Board.objects.filter(slug='paolo-roversi').count()
        # assert no result
        self.assertEqual(old_board, 0)



    def test_board_delete_with_wrong_user(self):
        """Test deletion of a board with a user which is not
        it's owner."""

        self.user2 = User.objects.create_user(
                username='toto',
                email='toto@lavilotte-rolle.fr',
                password='top_secret'
        )

        # login with user 2
        login = self.client.login(username='toto', password='top_secret')
        self.assertEqual(login, True)

        # get form
        response = self.client.get('/flr/paolo-roversi/delete/')

        # assert user has a 404 page
        self.assertEqual(response.status_code, 404)
        # get form and follow redirection
        response = self.client.get('/flr/paolo-roversi/delete/',
                follow=True
        )
        self.assertEqual(response.templates[0].name,
                '404.html'
        )

        # try to submit form
        response = self.client.post('/flr/paolo-roversi/delete/')
        # assert user has been redirected
        self.assertEqual(response.status_code, 404)

        # try to send form and follow redirection
        response = self.client.post('/flr/paolo-roversi/delete/',
                follow=True
        )

        self.assertEqual(response.templates[0].name,
                '404.html'
        )

        # assert board hasn't been deleted from db
        board = Board.objects.filter(slug='paolo-roversi').count()
        self.assertEqual(board, 1)
            



