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


    def test_get_sha1_hexdigest(self):
        to_hash = File(open(os.path.join(BASE_DIR, 'pin','test_files',
            'test.txt'), 'rb'))
        # get sha1 from file
        sha1 = get_sha1_hexdigest(to_hash)
        # assert everything is ok
        self.assertEqual(sha1, '368e0fcff6ac9f8eefc09e1ff59a8873566922d6')
        self.assertEqual(len(sha1), 40)




class ResourceTest(TestCase):
    """Resource model and views tests."""

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
        
        # create one board for each user
        self.board = Board(
                title="user board",
                description="user board for tests",
                policy=1,
                user=self.user)
        self.board.save()

        self.board2 = Board(
                title="user2 board",
                description="user2 board for tests",
                policy=1,
                user=self.user2)
        self.board2.save()


    def login(self, user):
        """Login with given user, assert it's ok"""
        login = self.client.login(username=user.username,
                password='top_secret')
        self.assertEqual(login, True)



    def test_urls(self):
        """Test urls and their templates."""
        urls = [
             # to reactivate when login page will work 
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
            {
                'url': '/pin/create/1/',
                'status': 302,
                'template': '404.html',
            },
        ]

        for elem in urls:
            response = self.client.get(elem['url'])
            self.assertEqual(response.status_code, elem['status'])
            response = self.client.get(elem['url'], follow=True)
            self.assertEqual(response.templates[0].name, elem['template'])


    def test_resource_upload(self):
        """Test upload of a resource file."""
        # login with user
        self.login(self.user)

        # go to choose origin page
        response = self.client.get('/pin/choose-origin/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                'pin/pin_choose_origin.html')

        # go to resource upload page
        response = self.client.get('/pin/upload/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'board/board_forms.html')
        
        def post_image():
            # post an image file
            with open(os.path.join(BASE_DIR, 'pin',
                'test_files', 'test.jpg'), 'rb') as fp:
                self.client.post('/pin/upload/', {'source_file': fp})
            self.assertEqual(response.status_code, 200)

        # post image file
        post_image()

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
        post_image()

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
        
        # get resource
        resource = Resource.objects.get(
                sha1='f5fbd1897ef61b69f071e36295342571e81017b9')

        # test set_previews_filename
        filename = set_previews_filename(resource)
        self.assertEqual(filename,
                'f5fbd1897ef61b69f071e36295342571e81017b9.jpg')

        # test set_previews_subdirs
        subdirs = set_previews_subdirs(resource)
        self.assertEqual(subdirs, 'f5/fb/')

        # test pin creation with new resource
        response = self.client.get('/pin/create/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_create.html')
        # assert no other users in board select
        self.assertEqual(response.context['form'].fields['board']._queryset.count(), 1)
        self.assertEqual(response.context['form'].fields['board']._queryset[0].pk, 1)

        # assert ressource is in context
        self.assertEqual(response.context['resource'], resource)

        # test pin creation with not existing resource
        response = self.client.get('/pin/create/22/')
        self.assertEqual(response.status_code, 404)

        # test pin creation
        response = self.client.post('/pin/create/1/', {
            'board': self.board.pk,
            'description': 'Description of pin',
            }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_list.html')
        # assert pin is in db
        pins = Pin.objects.filter(resource=resource, board=self.board.pk,
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

        # test pin creation with a board which isn't user's one
        response = self.client.post('/pin/create/1/', {
            'board': self.board2.pk,
            'description': 'Try to post a pin on a board which isn\'t mine',
            }, follow=True)
        # assert form is served again
        self.assertEqual(response.templates[0].name, '404.html')
        # assert no pin has been saved
        pins = Pin.objects.all().count()
        self.assertEqual(pins, 1)

        # test pin creation with a resource which doesn't exists
        response = self.client.post('/pin/create/2/', {
            'board': self.board.pk,
            'description': 'Try to post a pin with an inexisting resource.',
            }, follow=True)
        self.assertEqual(response.templates[0].name, '404.html')



        
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

        def remove_empty_folders(path):
            # remove empty subfolders
            files = os.listdir(path)
            if len(files):
                for f in files:
                    fullpath = os.path.join(path, f)
                    if os.path.isdir(fullpath):
                        remove_empty_folders(fullpath)

            # if folder is empty, delete it
            files = os.listdir(path)
            if len(files) == 0:
                print('Remove empty folder: {}'.format(path))
                os.rmdir(path)

        remove_empty_folders(path)







