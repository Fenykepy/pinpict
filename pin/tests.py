import os

from django.test import TestCase, Client
from django.core.files import File

from pinpict.settings import BASE_DIR, MEDIA_ROOT
from user.models import User
from board.models import Board
from pin.models import Pin, Resource
from pin.utils import extract_domain_name, get_sha1_hexdigest


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
        self.assertEqual(os.path.isfile(os.path.join(MEDIA_ROOT,
            'previews/full/f5/fb/f5fbd1897ef61b69f071e36295342571e81017b9.jpg')),
            True)

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

        # remove file from MEDIA_ROOT
        os.remove(os.path.join(MEDIA_ROOT,
            'previews/full/f5/fb/f5fbd1897ef61b69f071e36295342571e81017b9.jpg'))








