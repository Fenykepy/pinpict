import os

from PIL import Image

from django.test import TestCase, Client
from django.core.files import File

from pinpict.settings import BASE_DIR, MEDIA_ROOT, PREVIEWS_WIDTH, \
        PREVIEWS_CROP, PREVIEWS_ROOT
from user.models import User
from board.models import Board
from pin.models import Pin, Resource
from pin.utils import *



# to move to user.tests
def create_test_users(instance):
    """Create two users for running tests."""
    # create first user (staff)
    instance.user = User.objects.create_user(
            username='flr',
            email='pro@lavilotte-rolle.fr',
            password='top_secret'
    )
    instance.user.is_staff = True
    instance.user.save()

    # create second user (normal)
    instance.user2 = User.objects.create_user(
            username='toto',
            email='toto@lavilotte-rolle.fr',
            password='top_secret'
    )



# to move to user.tests
def login(instance, user):
    """Login with given user, assert it's ok"""
    login = instance.client.login(username=user.username,
            password='top_secret')
    instance.assertEqual(login, True)



# to move to board.tests
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



def create_test_resources(instance):
    """Create two resources for tests."""
    instance.resource = Resource(
        sha1='4a523fe9c50a2f0b1dd677ae33ea0ec6e4a4b2a9',
        source_file='previews/full/4a/52/4a523fe9c50a2f0b1' +
        'dd677ae33ea0ec6e4a4b2a9.jpg',
    )
    instance.resource.save()

    instance.resource2 = Resource(
        sha1='757838b58a509a1f5bd144bf81311c6a2beb4adf',
        source_file='previews/full/75/78/757838b58a509a1' + 
        'f5bd144bf81311c6a2beb4adf.jpg',
    )
    instance.resource2.save()



def create_test_pins(instance):
    """Create two pins for tests.
    run create_test_boards and create_test_resources first.
    """
    instance.pin = Pin(
            resource = instance.resource,
            board = instance.board,
            description = 'Test pin for first board'
    )
    instance.pin.save()

    instance.pin2 = Pin(
            resource = instance.resource2,
            board = instance.board2,
            description = 'Test pin for second board'
    )
    instance.pin2.save()



def create_test_private_pins(instance):
    """Create two private pins for tests.
    run create_test_private_boards and create_test_resources first.
    """
    instance.privatePin = Pin(
            resource = instance.resource,
            board = instance.privateBoard,
            description = 'Test private pin'
    )
    instance.privatePin.save()

    instance.privatePin2 = Pin(
            resource = instance.resource2,
            board = instance.privateBoard,
            description = 'Second test private pin'
    )
    instance.privatePin2.save()



def test_urls(instance, urls):
    """Test urls."""
    for elem in urls:
        response = instance.client.get(elem['url'])
        instance.assertEqual(response.status_code, elem['status'])
        response = instance.client.get(elem['url'], follow=True)
        instance.assertEqual(response.templates[0].name, elem['template'])




class UtilsTest(TestCase):
    """Utils functions test."""

    def setUp(self):
        create_test_resources(self)


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


    def test_get_sha1_hexdigest(self):
        to_hash = File(open(os.path.join(BASE_DIR, 'pin','test_files',
            'test.txt'), 'rb'))
        # get sha1 from file
        sha1 = get_sha1_hexdigest(to_hash)
        # assert everything is ok
        self.assertEqual(sha1, '368e0fcff6ac9f8eefc09e1ff59a8873566922d6')
        self.assertEqual(len(sha1), 40)


    def test_set_previews_filename(self):
        filename = set_previews_filename(self.resource)
        self.assertEqual(filename,
                '4a523fe9c50a2f0b1dd677ae33ea0ec6e4a4b2a9.jpg')


    def test_set_previews_subdirs(self):
        subdirs = set_previews_subdirs(self.resource)
        self.assertEqual(subdirs, '4a/52/')




class ResourceTest(TestCase):
    """Resource model and views tests."""

    def setUp(self):
        # create users
        create_test_users(self)
        # launch client
        self.client = Client()


    def test_urls(self):
        urls = [
            {
                'url': '/pin/choose-origin/',
                'status': 302,
                'template': '404.html',
            },
            {
                'url': '/pin/upload/',
                'status': 302,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)

    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)

        urls = [
            {
                'url': '/pin/choose-origin/',
                'status': 200,
                'template': 'pin/pin_choose_origin.html',
            },
            {
                'url': '/pin/upload/',
                'status': 200,
                'template': 'board/board_forms.html'
            },
        ]
        test_urls(self, urls)


    def test_resource_upload(self):
        """Test upload of a resource file."""
        # login with user
        login(self, self.user)

        def post_image():
            # post an image file
            with open(os.path.join(BASE_DIR, 'pin',
                'test_files', 'test.jpg'), 'rb') as fp:
                return self.client.post('/pin/upload/', {'source_file': fp})

        # post image file
        response = post_image()
        self.assertEqual(response.status_code, 302)

        # assert file has been save on hdd
        full = os.path.join(MEDIA_ROOT,
            'previews/full/f5/fb/f5fbd1897ef61b69f071e36295342571e81017b9.jpg')
        self.assertEqual(os.path.isfile(full), True)

        # assert previews have been generated and file size are good
        for preview in PREVIEWS_WIDTH:
            preview_file = os.path.join(MEDIA_ROOT, 'previews', preview[1],
                'f5/fb/f5fbd1897ef61b69f071e36295342571e81017b9.jpg')
            self.assertEqual(os.path.isfile(preview_file), True)
            img = Image.open(preview_file)
            width = img.size[0]
            # assert it's good width
            if preview[0] > 200:
                self.assertEqual(width, 200)
            else:
                self.assertEqual(img.size[0], preview[0])

        for preview in PREVIEWS_CROP:
            preview_file = os.path.join(MEDIA_ROOT, 'previews', preview[2],
                'f5/fb/f5fbd1897ef61b69f071e36295342571e81017b9.jpg')
            self.assertEqual(os.path.isfile(preview_file), True)
            img = Image.open(preview_file)
            width, height = img.size
            # assert it's good width and height
            self.assertEqual(width, preview[0])
            self.assertEqual(height, preview[1])

        # assert resource has been save in db
        resource = Resource.objects.get(
                sha1='f5fbd1897ef61b69f071e36295342571e81017b9')
        self.assertEqual(resource.source_file,
            'previews/full/f5/fb/f5fbd1897ef61b69f071e36295342571e81017b9.jpg')
        self.assertEqual(resource.width, 200)
        self.assertEqual(resource.height, 300)
        self.assertEqual(resource.size, 16628)


        # upload again same image
        response = post_image()
        self.assertEqual(response.status_code, 302)

        # assert no new file has been saved on hdd (with a similar name,
        # in case FyleSystemStorage didn't work
        path = os.path.join(MEDIA_ROOT, 'previews/full/f5/fb/')
        count = 0

        for file in os.listdir(path):
            if file[:40] == 'f5fbd1897ef61b69f071e36295342571e81017b9':
                count +=1
        # assert only one file is present
        self.assertEqual(count, 1)


        # assert no new entry has been saved in db
        resource = Resource.objects.filter(
                sha1='f5fbd1897ef61b69f071e36295342571e81017b9').count()
        self.assertEqual(resource, 1)
        
        
        # remove files from MEDIA_ROOT
        os.remove(os.path.join(MEDIA_ROOT,
            'previews/full/f5/fb/f5fbd1897ef61b69f071e36295342571e81017b9.jpg'))
        for preview in PREVIEWS_WIDTH:
            os.remove(os.path.join(MEDIA_ROOT, 'previews', preview[1],
                'f5/fb/f5fbd1897ef61b69f071e36295342571e81017b9.jpg'))

        for preview in PREVIEWS_CROP:
            os.remove(os.path.join(MEDIA_ROOT, 'previews', preview[2],
                'f5/fb/f5fbd1897ef61b69f071e36295342571e81017b9.jpg'))


        # remove empty folders from MEDIA_ROOT, 'previews'
        path = os.path.join(MEDIA_ROOT, 'previews')
        remove_empty_folders(path)




class PinCreationTest(TestCase):
    """Pin creation test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # create boards
        create_test_boards(self)
        # create resources
        create_test_resources(self)
        # launch client
        self.client = Client()



    def test_urls(self):
        urls = [
            {
                'url': '/pin/create/1/',
                'status': 302,
                'template': '404.html',
            },
            {
                'url': '/pin/create/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)



    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)

        urls = [
            # test pin creation with existing resource
            {
                'url': '/pin/create/1/',
                'status': 200,
                'template': 'pin/pin_create.html',
            },
            # test pin creation with no resource
            {
                'url': '/pin/create/',
                'status': 404,
                'template': '404.html',
            },
            # test pin creation with not existing resource
            {
                'url': '/pin/create/22/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_pin_creation(self):
        # login with user
        login(self, self.user)


        response = self.client.get('/pin/create/1/')
        # assert no other users' boards are in select
        self.assertEqual(response.context['form'].fields['board']._queryset.count(), 1)
        self.assertEqual(response.context['form'].fields['board']._queryset[0].pk, 1)

        # assert ressource is in context
        self.assertEqual(response.context['resource'], self.resource)

        # test pin creation
        response = self.client.post('/pin/create/1/', {
            'board': self.board.pk,
            'description': 'Description of pin',
            }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_list.html')
        # assert pin is in db
        pins = Pin.objects.filter(resource=self.resource, board=self.board,
            description='Description of pin').count()
        self.assertEqual(pins, 1)

        # assert resource n_pins has been updated
        resource = Resource.objects.get(pk=1)
        self.assertEqual(resource.n_pins, 1)

        # assert user n_pins has been updated
        user = User.objects.get(pk=1)
        self.assertEqual(user.n_pins, 1)

        # assert board n_pins has been updated
        board = Board.objects.get(pk=1)
        self.assertEqual(board.n_pins, 1)


    def test_pin_creation_with_wrong_board(self):
        response = self.client.post('/pin/create/1/', {
            'board': self.board2.pk,
            'description': 'Try to post a pin on a board which isn\'t mine',
            }, follow=True)
        # assert form is served again
        self.assertEqual(response.templates[0].name, '404.html')
        # assert no pin has been saved
        pins = Pin.objects.all().count()
        self.assertEqual(pins, 0)


    def test_pin_creation_with_unexisting_resource(self):
        response = self.client.post('/pin/create/2/', {
            'board': self.board.pk,
            'description': 'Try to post a pin with an inexisting resource.',
            }, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.templates[0].name, '404.html')



class PinUpdateTest(TestCase):
    """Pin update test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # create resources
        create_test_resources(self)
        # create boards
        create_test_boards(self)
        # create pins
        create_test_pins(self)
        # launch client
        self.client = Client()


    def test_urls(self):
        urls = [
            {
                'url': '/pin/1/edit/',
                'status': 302,
                'template': '404.html',
            },
            {
                'url': '/pin/302/edit/',
                'status': 302,
                'template': '404.html',
            },
            {
                'url': '/pin/edit/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user 1
        login(self, self.user)

        urls = [
            # try to update user's pin
            {
                'url': '/pin/1/edit/',
                'status': 200,
                'template': 'pin/pin_create.html',
            },
            # try to update another user's pin
            {
                'url': '/pin/2/edit/',
                'status': 404,
                'template': '404.html',
            },
            {
                'url': '/pin/302/edit/',
                'status': 404,
                'template': '404.html',
            },
            {
                'url': '/pin/edit/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_pin_update(self):
        # login with user
        login(self, self.user)
        
        response = self.client.get('/pin/1/edit/')
        # assert no other users' boards are in select
        self.assertEqual(response.context['form'].fields['board']._queryset.count(), 1)
        self.assertEqual(response.context['form'].fields['board']._queryset[0].pk, 1)

        # assert resource is in context
        self.assertEqual(response.context['resource'], self.resource)

        # test post
        response = self.client.post('/pin/1/edit/', {
            'board': self.board.pk,
            'description': 'New description',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_view.html')
        # assert change have been save in db
        pin = Pin.objects.get(pk=1)
        self.assertEqual(pin.description, 'New description')


    def test_pin_update_with_wrong_board(self):
        # login with user
        login(self, self.user)
        
        response = self.client.post('/pin/1/edit/', {
            'board': self.board2.pk,
            'description': 'New description',
        }, follow=True)
        self.assertEqual(response.status_code, 404)
        # assert change hasn't been save in db
        pin = Pin.objects.get(pk=1)
        self.assertEqual(pin.board, self.board)


    def test_pin_update_with_wrong_user(self):
        # login with user
        login(self, self.user)

        response = self.client.post('/pin/2/edit/', {
            'board': self.board2.pk,
            'description': 'New description',
        }, follow=True)
        self.assertEqual(response.status_code, 404)
        # assert change hasn't been save in db
        pin = Pin.objects.get(pk=2)
        self.assertEqual(pin.description, 'Test pin for second board')



class PinDeleteTest(TestCase):
    """Pin deletion test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # create resources
        create_test_resources(self)
        # create boards
        create_test_boards(self)
        # create pins
        create_test_pins(self)
        # launch client
        self.client = Client()


    def test_urls(self):
        urls = [
            {
                'url': '/pin/1/delete/',
                'status': 302,
                'template': '404.html',
            },
            {
                'url': '/pin/372/delete/',
                'status': 302,
                'template': '404.html',
            },
            {
                'url': '/pin/delete/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user 1
        login(self, self.user)

        urls = [
            # try to delete user's pin
            {
                'url': '/pin/1/delete/',
                'status': 200,
                'template': 'pin/pin_delete.html',
            },
            # try to delete pin which doen't exist
            {
                'url': '/pin/372/delete/',
                'status': 404,
                'template': '404.html',
            },
            # try to delete another user's pin
            {
                'url': '/pin/2/delete/',
                'status': 404,
                'template': '404.html',
            },
            {
                'url': '/pin/delete/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_pin_delete(self):
        # login with user
        login(self, self.user)

        response = self.client.get('/pin/1/delete/')
        self.assertEqual(response.context['pin'], self.pin)

        response = self.client.post('/pin/1/delete/',
                follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'board/board_list.html')
        
        # assert pin has been deleted
        n_pins = Pin.objects.all().count()
        self.assertEqual(n_pins, 1)
        pins = Pin.objects.all()
        self.assertEqual(pins[0].pk, 2)

        # assert board n_pins, resource n_pins and user n_pins have been updated
        resource = Resource.objects.get(pk=1)
        self.assertEqual(resource.n_pins, 0)
        
        user = User.objects.get(pk=1)
        self.assertEqual(user.n_pins, 0)

        board = Board.objects.get(pk=1)
        self.assertEqual(board.n_pins, 0)


    def test_pin_delete_with_wrong_user(self):
        # login with user
        login(self, self.user)

        response = self.client.post('/pin/2/delete/')
        self.assertEqual(response.status_code, 404)
        
        # assert no pin has been deleted
        n_pins = Pin.objects.all().count()
        self.assertEqual(n_pins, 2)


    def test_pin_delete_with_unexisting_pin(self):
        # login with user
        login(self, self.user)

        response = self.client.post('/pin/673/delete/')
        self.assertEqual(response.status_code, 404)


class PinView(TestCase):
    """Pin view test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # create resources
        create_test_resources(self)
        # create boards
        create_test_boards(self)
        # create private boards
        create_test_private_boards(self)
        # create pins
        create_test_pins(self)
        # create private pins
        create_test_private_pins(self)
        # launch client
        self.client = Client()


    def test_urls(self):
        urls = [
            # public pin of user one
            {
                'url': '/pin/1/',
                'status': 200,
                'template': 'pin/pin_view.html',
            },
            # public pin of user two
            {
                'url': '/pin/2/',
                'status': 200,
                'template': 'pin/pin_view.html',
            },
            # private pin should raise 404
            {
                'url': '/pin/3/',
                'status': 404,
                'template': '404.html',
            },
            # not existing pin should raise 404
            {
                'url': '/pin/389/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)

        urls = [
            # public pin of user one
            {
                'url': '/pin/1/',
                'status': 200,
                'template': 'pin/pin_view.html',
            },
            # public pin of user two
            {
                'url': '/pin/2/',
                'status': 200,
                'template': 'pin/pin_view.html',
            },
            # private pin of user
            {
                'url': '/pin/3/',
                'status': 200,
                'template': 'pin/pin_view.html',
            },
            # not existing pin should raise 404
            {
                'url': '/pin/389/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)

        # login with user2
        login(self, self.user2)

        urls = [
            # private pin of other user
            {
                'url': '/pin/3/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_unlogged_pin_view(self):
        """Assert context shows good pin."""
        response = self.client.get('/pin/1/')
        self.assertEqual(response.context['pin'].pk, 1)


    def test_logged_in_pin_view(self):
        """Assert context shows good pin to logged in user."""
        # login with user
        login(self, self.user)
        # try to see user2 pin
        response = self.client.get('/pin/2/')
        self.assertEqual(response.context['pin'].pk, 2)


    def test_logged_in_private_pin_view(self):
        """Assert context shows good private pin to its owner."""
        # login with user
        login(self, self.user)
        # try to see private pin
        response = self.client.get('/pin/3/')
        self.assertEqual(response.context['pin'].pk, 3)



class PinList(TestCase):
    """Pin list test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # create resources
        create_test_resources(self)
        # create boards
        create_test_boards(self)
        # create private boards
        create_test_private_boards(self)
        # create pins
        create_test_pins(self)
        # create private pins
        create_test_private_pins(self)
        # launch client
        self.client = Client()


    # context shows good board,
    # context shows good private board to its owner
    # context raise 404 if another user ask for a private board
    pass






        

