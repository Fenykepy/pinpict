from django.test import TestCase, Client

from user.models import User
from user.tests import create_test_users, login, test_urls
from board.models import Board
from pin.models import Pin, Resource



def create_test_boards(instance):
    """Create one test board for each user.
    run create_test_users first.
    """
    instance.board = Board(
            title='user board',
            description='user board for tests',
            policy=1,
            user = instance.user)
    instance.board.save()

    instance.board2 = Board(
            title='user2 board',
            description='user2 board for tests',
            policy=1,
            user = instance.user2)
    instance.board2.save()



def create_test_private_boards(instance):
    """Create one test private board for first user.
    run create_test_users first.
    """
    instance.privateBoard = Board(
            title='private board',
            description='user private board for tests',
            policy=0,
            user = instance.user)
    instance.privateBoard.save()




class BoardCreationTest(TestCase):
    """Board app tests."""

    def setUp(self):
        # create users
        create_test_users(self)
        # start client
        self.client = Client()


    def test_urls(self):
        urls = [
            # create public board
            {
                'url': '/board/create/',
                'status': 302,
                'template': 'user/user_login.html',
            },
            # create private board
            {
                'url': '/board/create/private/',
                'status': 302,
                'template': 'user/user_login.html',
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)

        urls = [
            # create public board
            {
                'url': '/board/create/',
                'status': 200,
                'template': 'board/board_forms.html',
            },
            # create private board
            {
                'url': '/board/create/private/',
                'status': 200,
                'template': 'board/board_forms.html',
            },
        ]


    def test_public_board_creation(self):
        # login with user
        login(self, self.user)

        response = self.client.post('/board/create/', {
            'title': 'Richard Avedon',
            'description': 'Photographs of Richard Avedon',
            }, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                'board/board_list.html'
        )

        # assert board has been saved in db
        board = Board.publics.get(slug='richard-avedon')
        # assert user is good one
        self.assertEqual(board.user.username, 'flr')
        # assert policy is good one
        self.assertEqual(board.policy, 1)
        # assert it doesn't appear in private boards
        board = Board.privates.filter(slug='richard-avedon').count()
        self.assertEqual(board, 0)
        # assert user n_boars has been updated
        user = User.objects.get(username='flr')
        self.assertEqual(user.n_boards, 1)
        self.assertEqual(user.n_public_boards, 1)


    def test_private_board_creation(self):
        # login with user
        login(self, self.user)

        response = self.client.post('/board/create/private/', {
            'title': 'Richard Avedon',
            'description': 'Photographs of Richard Avedon',
            }, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                'board/board_list.html'
        )

        # assert board has been saved in db
        board = Board.privates.get(slug='richard-avedon')
        # assert user is good one
        self.assertEqual(board.user.username, 'flr')
        # assert policy is good one
        self.assertEqual(board.policy, 0)
        # assert it doesn't appear in private boards
        board = Board.publics.filter(slug='richard-avedon').count()
        self.assertEqual(board, 0)
        # assert user n_boars has been updated
        user = User.objects.get(username='flr')
        self.assertEqual(user.n_boards, 1)
        self.assertEqual(user.n_public_boards, 0)




            


class BoardUpdateTest(TestCase):
    """Board app tests."""

    def setUp(self):
        # create users
        create_test_users(self)
        # create boards
        create_test_boards(self)
        # create private boards
        create_test_private_boards(self)
        # start client
        self.client = Client()


    def test_urls(self):
        urls = [
            # try to update existing user and board
            {
                'url': '/flr/user-board/edit/',
                'status': 302,
                'template': 'user/user_login.html',
            },
            # try to update existing user and board with wrong user
            {
                'url': '/toto/user-board/edit/',
                'status': 302,
                'template': 'user/user_login.html',
            },
            # try to update existing user and unexisting board
            {
                'url': '/toto/my-beautiful-board/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)

        urls = [
            # try to update existing user and board
            {
                'url': '/flr/user-board/edit/',
                'status': 200,
                'template': 'board/board_forms.html',
            },
            # try to update existing user and board with wrong user
            {
                'url': '/toto/user-board/edit/',
                'status': 404,
                'template': '404.html',
            },
            # try to update existing user and unexisting board
            {
                'url': '/toto/my-beautiful-board/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_board_update(self):
        # login with user
        login(self, self.user)

        response = self.client.post('/flr/user-board/edit/', {
            'title': 'Paolo Roversi',
            'description': 'Photographs of Paolo Roversi',
            'policy': 1,
            }, follow=True
        )

        # assert redirection is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                'board/board_list.html'
        )
        # assert update has been saved in db
        board = Board.objects.get(slug='paolo-roversi')
        # assert description is ok
        self.assertEqual(board.description, 'Photographs of Paolo Roversi')

        ## try to change policys
        # assert board is public
        self.assertEqual(board.policy, 1)
        board = Board.publics.filter(slug='paolo-roversi').count()
        self.assertEqual(board, 1)

        # change board policy
        response = self.client.post('/flr/paolo-roversi/edit/', {
            'title': 'Paolo Roversi',
            'description': 'Photographs of Paolo Roversi',
            'policy': 0,
            }, follow=True
        )

        # assert redirection is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                'board/board_list.html'
        )

        # assert board is now private
        board = Board.publics.filter(slug='paolo-roversi').count()
        self.assertEqual(board, 0)
        board = Board.privates.filter(slug='paolo-roversi').count()
        self.assertEqual(board, 1)


    def test_board_update_with_wrong_user(self):
        # login with user2
        login(self, self.user2)

        response = self.client.post('/flr/user-board/edit/', {
            'title': 'New Title',
            'description': 'New description',
            'policy': 1,
            }
        )
        self.assertEqual(response.status_code, 404)

        # assert changes haven't been save in db
        board = Board.objects.filter(title='New Title').count()
        self.assertEqual(board, 0)
        # assert old board still exists
        board = Board.objects.filter(title='user board').count()
        self.assertEqual(board, 1)



class BoardDeleteTest(TestCase):
    """Board app tests."""

    def setUp(self):
        # create users
        create_test_users(self)
        # create boards
        create_test_boards(self)
        # start client
        self.client = Client()


    def test_urls(self):
        urls = [
            # try to delete existing board
            {
                'url': '/flr/user-board/delete/',
                'status': 302,
                'template': 'user/user_login.html',
            },
            # try to delete unexisting board
            {
                'url': '/toto/user-board/delete/',
                'status': 302,
                'template': 'user/user_login.html',
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)

        urls = [
            # try to delete existing board
            {
                'url': '/flr/user-board/delete/',
                'status': 200,
                'template': 'board/board_delete.html',
            },
            # try to delete unexisting board with unexisting user
            {
                'url': '/tartempion/false-board/delete/',
                'status': 404,
                'template': '404.html',
            },
            # try to delete wrong board with wrong user
            {
                'url': '/toto/user-board/delete/',
                'status': 404,
                'template': '404.html',
            },
            # try to delete board of another user
            {
                'url': '/flr/user2-board/delete/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_board_delete(self):
        # login with user
        login(self, self.user)

        # get board
        board = Board.objects.get(slug='user-board')
        # create test resource
        resource = Resource(
                sha1 = 'toto',
                source_file = 'toto.jpg',
        )
        resource.save()

        # create 3 test pins for the board
        pin = Pin(
                resource = resource,
                board = board,
                description = 'pin1',
                pin_user = self.user,
        )
        pin.save()

        pin2 = Pin(
                resource = resource,
                board = board,
                description = 'pin2',
                pin_user = self.user,
        )
        pin2.save()

        pin3 = Pin(
                resource = resource,
                board = board,
                description = 'pin3',
                pin_user = self.user,
        )
        pin3.save()
        
        # assert pins have been created
        n_pins = Pin.objects.all().count()
        self.assertEqual(n_pins, 3)

        response = self.client.post('/flr/user-board/delete/',
                follow=True
        )

        # assert redirection is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                'board/board_list.html'
        )
        # assert board has been deleted from db
        old_board = Board.objects.filter(slug='user-board').count()
        # assert no result
        self.assertEqual(old_board, 0)
        # assert user n_boards has been updated
        user = User.objects.get(username='flr')
        self.assertEqual(user.n_boards, 0)
        self.assertEqual(user.n_public_boards, 0)
        # assert board pins have been deleted
        n_pins = Pin.objects.all().count()
        self.assertEqual(n_pins, 0)




    def test_board_delete_with_wrong_user(self):
        # login with user2
        login(self, self.user2)

        response = self.client.post('/flr/user-board/delete/',
                follow=True
        )

        # assert redirection is ok
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.templates[0].name,
                '404.html'
        )

        # assert board hasn't been deleted from db
        board = Board.objects.filter(slug='user-board').count()
        self.assertEqual(board, 1)



class BoardListTest(TestCase):
    """Board app tests."""

    def setUp(self):
        # create users
        create_test_users(self)
        # create boards
        create_test_boards(self)
        # create private boards
        create_test_private_boards(self)
        # start client
        self.client = Client()


    def test_urls(self):
        urls = [
            {
                'url': '/flr/',
                'status': 200,
                'template': 'board/board_list.html',
            },
            # unknown user should return 404
            {
                'url': '/tom/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_board_list_with_standard_user(self):
        # login with user2
        login(self, self.user2)

        response = self.client.get('/flr/')
        self.assertEqual(response.status_code, 200)
        # assert we have public boards
        self.assertEqual(len(response.context['boards']), 1)
        self.assertEqual(response.context['boards'][0].title, 'user board')
        # assert we don't have private boards
        self.assertEqual(hasattr(response.context, 'private_boards'), False)


    def test_board_list_with_owner_user(self):
        # login with user
        login(self, self.user)

        response = self.client.get('/flr/')
        self.assertEqual(response.status_code, 200)
        # assert we have public boards
        self.assertEqual(len(response.context['boards']), 1)
        self.assertEqual(response.context['boards'][0].title, 'user board')
        # assert we have private boards
        self.assertEqual(len(response.context['private_boards']), 1)
        self.assertEqual(response.context['private_boards'][0].title,
                'private board')


