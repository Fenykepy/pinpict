from django.test import TestCase, Client

from user.models import User
from board.models import Board


class BoardTest(TestCase):
    """Board app tests."""

    def setUp(self):
        # create first user
        self.user = User.objects.create_user(
                username='flr',
                email='pro@lavilotte-rolle.fr',
                password='top_secret'
        )
        self.user.website = 'http://lavilotte-rolle.fr'
        self.user.save()
        
        # create a second user
        self.user2 = User.objects.create_user(
                username='toto',
                email='toto@lavilotte-rolle.fr',
                password='top_secret'
        )


        # create a public board
        board = Board()
        board.title = 'Paolo Roversi'
        board.description = 'Photographies de Paolo Roversi.'
        board.policy = 1
        board.user = self.user
        board.save()
 
        # create a private board
        board = Board()
        board.title = 'My private board'
        board.description = 'Private board'
        board.policy = 0
        board.user = self.user
        board.save()
               
        # start client
        self.client = Client()



    def login(self, user):
        """Login with given user, assert it's ok"""
        login = self.client.login(username=user.username,
                password='top_secret')
        self.assertEqual(login, True)



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
                'template': 'pin/pin_list.html',
            },
            # unknown user should return 404
            {
                'url': '/tom/',
                'status': 404,
                'template': '404.html',
            },
            # unknown user with known board should return 404
            {
                'url': '/tom/paolo-roversi/',
                'status': 404,
                'template': '404.html',
            },
            # unknown user with unknown board should return 404
            {
                'url': '/tom/tom-board/',
                'status': 404,
                'template': '404.html',
            },
            # known user with unknown board should return 404
            {
                'url': '/flr/tom-board/',
                'status': 404,
                'template': '404.html',
            },
            # known user with known board which doesn't belong to him
            # should return 404
            {
                'url': '/toto/paolo-roversi/',
                'status': 404,
                'template': '404.html',
            },
            {
                'url': '/board/create/',
                'status': 302,
                'template': '404.html',
            },
            {
                'url': '/board/create/private/',
                'status': 302,
                'template': '404.html',
            },
            {
               'url': '/flr/paolo-roversi/edit/',
               'status': 302,
               'template': '404.html',
            },
            {
               'url': '/flr/paolo-roversi/delete/',
               'status': 302,
               'template': '404.html',
            },
            
        ]

        for elem in urls:
            response = self.client.get(elem['url'])
            self.assertEqual(response.status_code, elem['status'])
            response = self.client.get(elem['url'], follow=True)
            self.assertEqual(response.templates[0].name, elem['template'])


    def test_board_list_with_standard_user(self):
        """Test board list context."""
        # login with not owner user
        self.login(self.user2)

        # go to board list page
        response = self.client.get('/flr/')
        self.assertEqual(response.status_code, 200)
        # assert we have public boards
        self.assertEqual(len(response.context['boards']), 1)
        self.assertEqual(response.context['boards'][0].title, 'Paolo Roversi')
        # assert we don't have private boards
        self.assertEqual(hasattr(response.context, 'private_boards'), False)



    def test_board_list_with_owner_user(self):
        """Test board list context."""
        # login with not owner user
        self.login(self.user)

        # go to board list page
        response = self.client.get('/flr/')
        self.assertEqual(response.status_code, 200)
        # assert we have public boards
        self.assertEqual(len(response.context['boards']), 1)
        self.assertEqual(response.context['boards'][0].title, 'Paolo Roversi')

        # assert we have private boards
        self.assertEqual(len(response.context['private_boards']), 1)
        self.assertEqual(response.context['private_boards'][0].title,
                'My private board')



    def test_public_board_creation(self):
        """Test new board creation."""
        # login
        self.login(self.user)

        # send form
        response = self.client.post('/board/create/', {
            'title': 'Richard Avedon',
            'description': 'Photographies de Richard Avedon',
            }, follow=True
        )
        # assert redirection is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                'board/board_list.html'
        )
        # assert board has been saved in db
        new_board = Board.publics.get(slug='richard-avedon')
        # assert user is the good one
        self.assertEqual(new_board.user.username, 'flr')
        # assert policy is good one
        self.assertEqual(new_board.policy, 1)
        # assert it doesn't appears in private boards list
        board = Board.privates.filter(slug='richard-avedon').count()
        self.assertEqual(board, 0)
        # assert user n_boards has been updated
        user = User.objects.get(username='flr')
        self.assertEqual(user.n_boards, 3)



    def test_private_board_creation(self):
        """Test new private board creation."""
        # login
        self.login(self.user)

        # send form
        response = self.client.post('/board/create/private/', {
            'title': 'Richard Avedon',
            'description': 'photographies de Richard Avedon',
            }, follow=True
        )
        # assert redirection is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                'board/board_list.html'
        )
        # assert board has been saved in db
        new_board = Board.privates.get(slug='richard-avedon')
        # assert user is the good one
        self.assertEqual(new_board.user.username, 'flr')
        # assert policy is good one
        self.assertEqual(new_board.policy, 0)
        # assert it doesn't appears in public boards list
        board = Board.publics.filter(slug='richard-avedon').count()
        self.assertEqual(board, 0)




    def test_board_update(self):
        """Test board update."""
        # login
        self.login(self.user)

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

        ## try to change policy in two directions
        # assert board is public
        board = Board.publics.filter(slug='paolo-roversi').count()
        self.assertEqual(board, 1)

        ## send form
        response = self.client.post('/flr/paolo-roversi/edit/', {
            'title': 'Paolo Roversi',
            'description': 'Photographies de Paolo Roversi :)',
            'policy': 0,
            }, follow=True
        )

        # assert redirection is ok
        self.assertEqual(response.status_code, 200)
        
        # assert board is private 
        public_board = Board.publics.filter(slug='paolo-roversi').count()
        self.assertEqual(public_board, 0)
        private_board = Board.privates.filter(slug='paolo-roversi').count()
        self.assertEqual(private_board, 1)


        ## send form
        response = self.client.post('/flr/paolo-roversi/edit/', {
            'title': 'Paolo Roversi',
            'description': 'Photographies de Paolo Roversi :)',
            'policy': 1,
            }, follow=True
        )

        # assert redirection is ok
        self.assertEqual(response.status_code, 200)
        
        # assert board is private 
        public_board = Board.publics.filter(slug='paolo-roversi').count()
        self.assertEqual(public_board, 1)
        private_board = Board.privates.filter(slug='paolo-roversi').count()
        self.assertEqual(private_board, 0)





    def test_board_update_with_wrong_user(self):
        """Test board update with a user which is not owner of board."""
        # login with user 2
        self.login(self.user2)
        
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
        self.login(self.user)

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

        # login with user 2
        self.login(self.user2)

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
            



