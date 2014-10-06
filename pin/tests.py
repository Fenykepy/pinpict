import os


from wand.image import Image

from django.test import TestCase, Client
from django.core.files import File

from pinpict.settings import BASE_DIR, MEDIA_ROOT, PREVIEWS_WIDTH, \
        PREVIEWS_CROP, PREVIEWS_ROOT

from user.models import User
from user.tests import create_test_users, login, test_urls
from board.models import Board
from board.tests import create_test_boards, create_test_private_boards
from pin.models import Pin, Resource
from pin.utils import *



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
            description = 'Test pin for first board',
            pin_user = instance.user,
            policy = instance.board.policy
    )
    instance.pin.save()

    instance.pin2 = Pin(
            resource = instance.resource2,
            board = instance.board2,
            description = 'Test pin for second board',
            pin_user = instance.user2,
            policy = instance.board.policy
    )
    instance.pin2.save()



def create_test_private_pins(instance):
    """Create two private pins for tests.
    run create_test_private_boards and create_test_resources first.
    """
    instance.privatePin = Pin(
            resource = instance.resource,
            board = instance.privateBoard,
            description = 'Test private pin',
            pin_user = instance.user,
            policy = instance.board.policy

    )
    instance.privatePin.save()

    instance.privatePin2 = Pin(
            resource = instance.resource2,
            board = instance.privateBoard,
            description = 'Second test private pin',
            pin_user = instance.user,
            policy = instance.board.policy
    )
    instance.privatePin2.save()



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
        with open(os.path.join(BASE_DIR, 'pin', 'test_files',
            'test.txt'), 'rb') as fb:
            to_hash = File(fb)
            # get sha1 from file
            sha1 = get_sha1_hexdigest(to_hash)

        # assert everything is ok
        self.assertEqual(sha1, '368e0fcff6ac9f8eefc09e1ff59a8873566922d6')
        self.assertEqual(len(sha1), 40)

#
#    def test_set_previews_filename(self):
#        filename = set_previews_filename(self.resource)
#        self.assertEqual(filename,
#                '4a523fe9c50a2f0b1dd677ae33ea0ec6e4a4b2a9.jpg')
#
#
#    def test_set_previews_subdirs(self):
#        subdirs = set_previews_subdirs(self.resource)
#        self.assertEqual(subdirs, '4a/52/')
#

    def test_remove_empty_folders(self):
        # mkdirs for test
        test_dir = os.path.join(BASE_DIR, 'pin', 'test_files', 'test_dir')
        os.makedirs(test_dir)
        hierarchy1 = os.path.join(
            test_dir, 'folder1', 'subfolder1', 'subsubfolder1')
        os.makedirs(hierarchy1)
        hierarchy2 = os.path.join(
            test_dir, 'folder2', 'subfolder2', 'subsubfolder2')
        os.makedirs(hierarchy2)
        hierarchy3 = os.path.join(
            test_dir, 'folder3', 'subfolder3', 'subsubfolder3')
        os.makedirs(hierarchy3)
        # create a file for tests
        with open(os.path.join(test_dir, 'folder2', 'subfolder2', 'test.txt'),
            encoding='utf-8', mode='w') as a_file:
            a_file.write('test_file')
        # remove empty folders
        remove_empty_folders(test_dir)
        
        # assert file hasn't been removed
        file_path = os.path.join(
            test_dir, 'folder2', 'subfolder2', 'test.txt')
        self.assertEqual(os.path.exists(file_path), True)
        
        # assert empty folders have been removed
        self.assertEqual(os.path.exists(hierarchy1), False)
        self.assertEqual(os.path.exists(hierarchy2), False)
        self.assertEqual(os.path.exists(hierarchy3), False)

        # remove remaning files and dirs
        os.remove(file_path)
        os.rmdir(os.path.join(test_dir, 'folder2', 'subfolder2'))
        os.rmdir(os.path.join(test_dir, 'folder2'))
        os.rmdir(test_dir)


    def test_picture_html_parser(self):
        # make some html for test
        html = """
        <h1>My beautiful title</h1>
        <img src="/data/1.jpg" alt="" />
        <img src="http://lavilotte-rolle.fr/data/1.jpg" alt="http" />
        <img src="https://lavilotte-rolle.fr/data/1.jpg" alt="https" />
        <strong>some noise</strong>
        <a href="/data/1.jpg" title="">link</a>
        <a href="http://data/1.jpg" title="my link picture">link</a>
        <a href="https://data/1.jpg" title="my link picture">link</a>
        <a href="999.jpg" titlle="">link</a>
        <a href="./999.jpg">tanie</a>
        <a href="../7.jpg">naiet</a>
        <a href="../../7.jpg">naiet</a>
        """

        result = [
            {
                'href': 'http://www.lavilotte-rolle.fr/data/1.jpg',
                'alt': '',
            },
            {
                'href': 'http://lavilotte-rolle.fr/data/1.jpg',
                'alt': 'http',
            },
            {
                'href': 'https://lavilotte-rolle.fr/data/1.jpg',
                'alt': 'https',
            },
            {
                'href': 'http://www.lavilotte-rolle.fr/data/1.jpg',
                'alt': '',
            },
            {
                'href': 'http://data/1.jpg',
                'alt': 'my link picture',
            },
            {
                'href': 'https://data/1.jpg',
                'alt': 'my link picture',
            },
            {
                'href': 'http://www.lavilotte-rolle.fr/portfolio/999.jpg',
                'alt': '',
            },
            {
                'href': 'http://www.lavilotte-rolle.fr/portfolio/999.jpg',
                'alt': '',
            },
            {
                'href': 'http://www.lavilotte-rolle.fr/7.jpg',
                'alt': '',
            },
        ]

        
        parser = PictureHTMLParser(convert_charrefs=True)
        parser.pictures = []
        parser.url = 'http://www.lavilotte-rolle.fr/portfolio/'
        parser.protocol = 'http://'
        parser.url_path = 'www.lavilotte-rolle.fr/portfolio/'
        parser.root_url = 'http://www.lavilotte-rolle.fr'
        parser.feed(html)

        self.assertEqual(parser.pictures, result)



class PinCreationTest(TestCase):
    """Pin creation test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # create boards
        create_test_boards(self)
        # launch client
        self.client = Client()


    def previews_generation_test(self, resource):
        """Check that previews have correctly been generated."""
        for preview in PREVIEWS_WIDTH:
            preview_file = os.path.join(
                    MEDIA_ROOT,
                    'previews',
                    preview[1],
                    resource.previews_path
            )
            self.assertEqual(os.path.isfile(preview_file), True)
            with Image(filename=preview_file) as img:
                width = img.size[0]
            # assert preview is good size
            if preview[0] > resource.width:
                self.assertEqual(width, resource.width)
            else:
                self.assertEqual(width, preview[0])

        for preview in PREVIEWS_CROP:
            preview_file = os.path.join(
                    MEDIA_ROOT,
                    'previews',
                    preview[2],
                    resource.previews_path
            )
            self.assertEqual(os.path.isfile(preview_file), True)
            with Image(filename=preview_file) as img:
                width, height = img.size
            #a assert it's good size
            self.assertEqual(width, preview[0])
            self.assertEqual(height, preview[1])



    def remove_resource_files(self, resource):
        """Remove all remaning files from a resources
        (previews, resource itself)."""
        # remove resource
        os.remove(os.path.join(MEDIA_ROOT,
            resource.source_file.name))
        # remove previews
        for preview in PREVIEWS_WIDTH:
            os.remove(os.path.join(
                MEDIA_ROOT,
                'previews',
                preview[1],
                resource.previews_path
            ))
        for preview in PREVIEWS_CROP:
            os.remove(os.path.join(
                MEDIA_ROOT,
                'previews',
                preview[2],
                resource.previews_path
            ))
        # remove left empty folders
        remove_empty_folders(os.path.join(
            MEDIA_ROOT,
            'previews'
        ))





    def test_urls(self):
        urls = [
            {
                'url': '/pin/choose-origin/',
                'status': 302,
                'template': 'user/user_login.html',
            },
            {
                'url': '/pin/upload/',
                'status': 302,
                'template': 'user/user_login.html',
            },
            {
                'url': '/pin/create/',
                'status': 302,
                'template': 'user/user_login.html',
            },
            {
                'url': '/pin/create/1/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)



    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)
        # set session
        session = self.client.session
        session.save()

        urls = [
            # test pin choose origin
            {
                'url': '/pin/choose-origin/',
                'status': 200,
                'template': 'pin/pin_choose_origin.html',
            },
            # test pin creation with no resource, as no post and no session
            # variable, should return 404
            {
                'url': '/pin/create/',
                'status': 404,
                'template': '404.html',
            },
            # test pin creation with existing resource
            {
                'url': '/pin/create/1',
                'status': 404,
                'template': '404.html',
            },
            # test pin creation with not existing resource
            {
                'url': '/pin/create/22/',
                'status': 404,
                'template': '404.html',
            },
            # test tmp pin upload
            {
                'url': '/pin/upload/',
                'status': 200,
                'template': 'board/board_forms.html'
            },
        ]
        test_urls(self, urls)



    def test_pin_creation_from_upload(self):
        """Test upload of a resource file."""
        # login with user
        login(self, self.user)
        session = self.client.session

        def post_image(follow=False):
            # post an image file
            with open(os.path.join(BASE_DIR, 'pin',
                'test_files', 'test.jpg'), 'rb') as fp:
                return self.client.post('/pin/upload/', {
                    'file': fp
                    }, follow=follow
                )

        # post image file
        response = post_image()
        self.assertEqual(response.status_code, 302)

        # assert file has been save on hdd
        tmp = 'tmp/a7ed26bf64d26b6687316b14fdbbaf9630a5d03e'
        tmp_path = os.path.join(MEDIA_ROOT, tmp)
        self.assertEqual(os.path.isfile(tmp_path), True)
        self.assertEqual(self.client.session['pin_create_tmp_resource'], tmp)
 
        # post image file
        response = post_image(follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_create.html')
        self.assertEqual(response.context['src'], '/media/tmp/a7ed26bf64d26b6687316b14fdbbaf9630a5d03e')

        # post pin
        response = self.client.post('/pin/create/', {
            'board': self.board.pk,
            'description': 'Description of pin',
        }, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_list.html')
        # assert pin is in db
        pins = Pin.objects.filter(board=self.board, description='Description of pin')
        self.assertEqual(len(pins), 1)
        # assert resource n_pins has been updated
        resource = pins[0].resource
        self.assertEqual(resource.n_pins, 1)
        # assert user n_pins has been updated
        self.assertEqual(pins[0].pin_user.n_pins, 1)
        self.assertEqual(pins[0].pin_user.n_public_pins, 1)
        # assert board n_pins has been updated
        self.assertEqual(pins[0].board.n_pins, 1)
        # assert resource_file exists
        self.assertTrue(os.path.exists(os.path.join(MEDIA_ROOT,
            resource.source_file.name)))
        # assert resource file, size, width and height are stored in db
        self.assertEqual(resource.source_file.name,
            'previews/full/a7/ed/a7ed26bf64d26b6687316b14fdbbaf9630a5d03e.jpeg')
        self.assertEqual(resource.width, 1024)
        self.assertEqual(resource.height, 767)
        self.assertEqual(resource.size, 114896)
        # assert previews have been generated
        self.previews_generation_test(resource)
        
        # assert session variable 'pin_create_tmp_resource' has been deleted
        self.assertEqual(hasattr(self.client.session, 'pin_create_tmp_resource'), False)
        # assert temporary file has been deleted
        self.assertEqual(os.path.isfile(tmp_path), False)

        # post same image again
        response = post_image()
        self.assertEqual(response.status_code, 302)

        # assert file hasn't been save on hdd (clone)
        self.assertEqual(os.path.isfile(tmp_path), False)
        # assert no session variable 'pin_create_tmp_resource'
        self.assertEqual(hasattr(self.client.session, 'pin_create_tmp_resource'), False)
        # assert session variable pin_create_resource
        self.assertEqual(self.client.session['pin_create_resource'], 1)

        # post pin again
        response = self.client.post('/pin/create/', {
            'board': self.board.pk,
            'description': 'Description of pin',
        }, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_list.html')

        # delete tmp file if still any (in case of error)
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

        # remove resource remaning files
        self.remove_resource_files(resource)



    def test_pin_creation_from_user_other_pin(self):
        # create resources and pins
        create_test_resources(self)
        create_test_pins(self)
        # login with user
        login(self, self.user)
        response = self.client.post('/pin/create/', {
            'pin': self.pin.pk,
        }, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_create.html')
        # assert session variable has been set
        self.assertEqual(self.client.session['pin_create_resource'], self.pin.resource.pk)
        self.assertEqual(self.client.session['pin_create_source'], self.pin.source)
        self.assertEqual(hasattr(self.client.session, 'pin_create_added_via'), False)
        # assert no other users' boards are in select
        self.assertEqual(response.context['form'].fields['board']._queryset.count(), 1)
        self.assertEqual(response.context['form'].fields['board']._queryset[0].pk, 1)      
        # assert ressource is in context
        self.assertEqual(response.context['resource'], self.resource)
        # post pin
        response = self.client.post('/pin/create/', {
            'board': self.board.pk,
            'description': 'Description of pin',
        }, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_list.html')
        # assert pin is in db
        pins = Pin.objects.filter(board=self.board, description='Description of pin')
        self.assertEqual(len(pins), 1)
        # assert resource n_pins has been updated
        resource = pins[0].resource
        self.assertEqual(resource.n_pins, 2)
        # assert user n_pins has been updated
        self.assertEqual(pins[0].pin_user.n_pins, 2)
        self.assertEqual(pins[0].pin_user.n_public_pins, 2)
        # assert board n_pins has been updated
        self.assertEqual(pins[0].board.n_pins, 2)



    def test_pin_creation_from_other_user_pin(self):
        # create resources and pins
        create_test_resources(self)
        create_test_pins(self)
        # login with user
        login(self, self.user)
        response = self.client.post('/pin/create/', {
            'pin': self.pin2.pk,
        }, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_create.html')
        # assert session variable has been set
        self.assertEqual(self.client.session['pin_create_resource'], self.pin2.resource.pk)
        self.assertEqual(self.client.session['pin_create_source'], self.pin2.source)
        self.assertEqual(self.client.session['pin_create_added_via'], self.user2.pk) 
        # assert no other users' boards are in select
        self.assertEqual(response.context['form'].fields['board']._queryset.count(), 1)
        self.assertEqual(response.context['form'].fields['board']._queryset[0].pk, 1)           
        # assert ressource is in context
        self.assertEqual(response.context['resource'], self.pin2.resource)
        # post pin
        response = self.client.post('/pin/create/', {
            'board': self.board.pk,
            'description': 'Description of pin',
        }, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_list.html')
        # assert pin is in db
        pins = Pin.objects.filter(board=self.board, description='Description of pin')
        self.assertEqual(len(pins), 1)
        # assert resource n_pins has been updated
        resource = pins[0].resource
        self.assertEqual(resource.n_pins, 2)
        # assert user n_pins has been updated
        self.assertEqual(pins[0].pin_user.n_pins, 2)
        self.assertEqual(pins[0].pin_user.n_public_pins, 2)
        # assert board n_pins has been updated
        self.assertEqual(pins[0].board.n_pins, 2)



    def test_pin_creation_with_unexisting_file(self):
        # login with user
        login(self, self.user)
        # set session
        session = self.client.session
        session['pin_create_tmp_resource'] = 'tmp/nothing/'
        session.save()
        response = self.client.post('/pin/create/', {
            'board': self.board.pk,
            'description': 'Description of pin',
        }, follow = True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.templates[0].name, '404.html')



    def test_pin_creation_with_wrong_board(self):
        # login with user
        login(self, self.user)
        # set session
        session = self.client.session
        session['pin_create_resource'] = 1
        session.save()
        response = self.client.post('/pin/create/', {
            'board': self.board2.pk,
            'description': 'Try to post a pin on a board which isn\'t mine',
            }, follow=True)
        # assert form is served again
        self.assertEqual(response.templates[0].name, '404.html')
        # assert no pin has been saved
        pins = Pin.objects.all().count()
        self.assertEqual(pins, 0)



    def test_pin_creation_with_unexisting_resource(self):
        # login with user
        login(self, self.user)
        # set session
        session = self.client.session
        session['pin_create_resource'] = 6
        session.save()

        response = self.client.post('/pin/create/', {
            'board': self.board.pk,
            'description': 'Try to post a pin with an inexisting resource.',
            }, follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.templates[0].name, '404.html')



    def test_pin_creation_from_url(self):
        # login with user
        login(self, self.user)
        response = self.client.post('/pin/create/', {
            'url': 'http://lavilotte-rolle.fr/tmp/pinpict_tests/',
            'src': 'http://lavilotte-rolle.fr/tmp/pinpict_tests/999.jpg',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['pin_create_source'],
            'http://lavilotte-rolle.fr/tmp/pinpict_tests/')
        self.assertEqual(self.client.session['pin_create_src'],
            'http://lavilotte-rolle.fr/tmp/pinpict_tests/999.jpg')

        response = self.client.post('/pin/create/', {
            'board': self.board.pk,
            'description': 'Pinned from an url',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_list.html')
        # assert pin is now in db
        pins = Pin.objects.filter(board=self.board, description='Pinned from an url')
        self.assertEqual(len(pins), 1)
        # assert resource n_pins has been updated
        resource = pins[0].resource
        self.assertEqual(resource.n_pins, 1)
        # assert user n_pins has been updated
        self.assertEqual(pins[0].pin_user.n_pins, 1)
        self.assertEqual(pins[0].pin_user.n_public_pins, 1)
        # assert board n_pins has been updated
        self.assertEqual(pins[0].board.n_pins, 1)
        # assert resource file exists
        self.assertTrue(os.path.exists(os.path.join(MEDIA_ROOT,
            resource.source_file.name)))
        # assert resource file, size, width and height are stored in db
        self.assertEqual(resource.source_file.name,
                'previews/full/e9/4e/e94ec191e243cbd891dd1b32d77329b8ce65a52f.jpeg')
        self.assertEqual(resource.width, 500)
        self.assertEqual(resource.height, 329)
        self.assertEqual(resource.size, 39268)
        # assert previews have been generated
        self.previews_generation_test(resource)
        # assert session variables have been deleted
        self.assertEqual(hasattr(self.client.session, 'pin_create_source'), False)
        self.assertEqual(hasattr(self.client.session, 'pin_create_src'), False)


        # post same url and src again
        response = self.client.post('/pin/create/', {
            'url': 'http://lavilotte-rolle.fr/tmp/pinpict_tests/',
            'src': 'http://lavilotte-rolle.fr/tmp/pinpict_tests/999.jpg',
            'description': 'pin description',
        })
        self.assertEqual(response.status_code, 200)
        # assert description and board are in form as initial
        self.assertEqual(response.context['form'].initial['description'],
                'pin description')
        self.assertEqual(response.context['form'].initial['board'], 1)

        response = self.client.post('/pin/create/', {
            'board': self.board.pk,
            'description': 'pin description',
        }, follow=True)
        # assert new pin point to same resource
        pins = Pin.objects.filter(resource = resource)
        self.assertEqual(len(pins), 2)
        # assert n_pins have been updated
        resource = Resource.objects.get(pk=resource.id)
        self.assertEqual(resource.n_pins, 2)
        # assert user n_pins has been updated
        self.assertEqual(pins[0].pin_user.n_pins, 2)
        self.assertEqual(pins[0].pin_user.n_public_pins, 2)
        # assert board n_pins has been updated
        self.assertEqual(pins[0].board.n_pins, 2)


        # remove resource remaining files
        self.remove_resource_files(resource)




    def test_pin_creation_from_url_without_src(self):
        # login with user
        login(self, self.user)
        response = self.client.post('/pin/create/', {
            'url': 'http://lavilotte-rolle.fr/tmp/pinpict_tests/',
        }, follow=True)
        # assert it redirects to pin_find
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_find.html')


    def test_pin_creation_from_url_without_url(self):
        # login with user
        login(self, self.user)
        response = self.client.post('/pin/create/', {
            'src': 'http://lavilotte-rolle.fr/tmp/pinpict_tests/',
        })
        # assert 404 is raised
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
                'template': 'user/user_login.html',
            },
            {
                'url': '/pin/302/edit/',
                'status': 302,
                'template': 'user/user_login.html',
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
                'template': 'user/user_login.html',
            },
            {
                'url': '/pin/372/delete/',
                'status': 302,
                'template': 'user/user_login.html',
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
        self.assertEqual(response.templates[0].name, 'pin/pin_list.html')
        
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
        self.assertEqual(user.n_public_pins, 0)

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


class PinViewTest(TestCase):
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
            # private pin of other user should raise 404
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
        # test links to next and previous pins
        self.assertEqual(response.context['next'], False)
        self.assertEqual(response.context['prev'], False)


    def test_prev_next_links(self):
        """Assert prev and next links are ok."""
        pin2 = Pin(
                resource = self.resource,
                board = self.board,
                description = 'Test pin for first board',
                pin_user = self.user,
                policy = self.board.policy
        )
        pin2.save()
        pin3 = Pin(
                resource = self.resource,
                board = self.board,
                description = 'Test pin for first board',
                pin_user = self.user,
                policy = self.board.policy
        )
        pin3.save()

        response = self.client.get('/pin/1/')
        # first pin, must have a next link but no prev one
        self.assertEqual(response.context['next'], 5)
        self.assertEqual(response.context['prev'], False)

        response = self.client.get('/pin/5/')
        # middle pin, must have next and prev link
        self.assertEqual(response.context['next'], 6)
        self.assertEqual(response.context['prev'], 1)

        response = self.client.get('/pin/6/')
        # last pin, must have prev link but no next one
        self.assertEqual(response.context['next'], False)
        self.assertEqual(response.context['prev'], 5)





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


class ListUserPins(TestCase):
    """User pin list test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # create resources(self)
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
            {
                'url': '/flr/pins/',
                'status': 200,
                'template': 'pin/pin_user_list.html',
            },
            {
                'url': '/tartempion/pins/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)

    def test_pin_list_context(self):
        """Assert context shows good pins."""
        response = self.client.get('/flr/pins/')
        self.assertEqual(len(response.context['pins']), 1)



class ListBoardPins(TestCase):
    """Board pin list test class."""

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
            # public board's pins list
            {
                'url': '/flr/user-board/',
                'status': 200,
                'template': 'pin/pin_list.html',
            },
            # private board's pins list !!! to change after creating login page !!!
            {
                'url': '/flr/private-board/',
                'status': 404,
                'template': '404.html',
            },
            # not existing board and user
            {
                'url': '/tartempion/board54/',
                'status': 404,
                'template': '404.html',
            },
            # not existing board with existing user
            {
                'url': '/flr/unexisting-board/',
                'status': 404,
                'template': '404.html',
            },
            # not existing user with existing board
            {
                'url': '/tartempion/user-board/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)

        urls = [
            # public board of user
            {
                'url': '/flr/user-board/',
                'status': 200,
                'template': 'pin/pin_list.html',
            },
            # public board of other user
            {
                'url': '/toto/user2-board/',
                'status': 200,
                'template': 'pin/pin_list.html',
            },
            # private board of user
            {
                'url': '/flr/private-board/',
                'status': 200,
                'template': 'pin/pin_list.html',
            },
        ]
        test_urls(self, urls)
        
        # login with user2
        login(self, self.user2)

        urls = [
            # private board of other user
            {
                'url': '/flr/private-board/',
                'status': 404,
                'template': '404.html',
            },
        ]
        test_urls(self, urls)


    def test_pin_list_context(self):
        """Assert context shows good pins."""
        response = self.client.get('/flr/user-board/')
        self.assertEqual(response.context['board'].slug, 'user-board')


class PinChooseUrlTest(TestCase):
    """Pin choose Url Test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # launch client
        self.client = Client()


    def test_urls(self):
        urls = [
            {
                'url': '/pin/url/',
                'status': 302,
                'template': 'user/user_login.html',
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)

        urls = [
            {
                'url': '/pin/url/',
                'status': 200,
                'template': 'board/board_forms.html',
            },
        ]
        test_urls(self, urls)


    def test_unlogged_url_choice(self):

        response = self.client.post('/pin/url/', {
            'url': 'http://www.lavilotte-rolle.fr',
            }
        )
        # should redirect to login page
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/pin/url/', {
            'url': 'http://www.lavilotte-rolle.fr',
            }, follow=True
        )
        self.assertEqual(response.templates[0].name,
                'user/user_login.html')


    def test_logged_in_url_choice(self):
        # login with user
        login(self, self.user)

        response = self.client.post('/pin/url/', {
            'url': 'http://www.lavilotte-rolle.fr',
            }
        )
        # should redirect to find page
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/pin/url/', {
            'url': 'http://www.lavilotte-rolle.fr',
            }, follow=True
        )
        # should redirect to pin_find page with url as parameter
        self.assertEqual(response.request['PATH_INFO'], '/pin/find/')
        self.assertEqual(response.request['QUERY_STRING'],
                'url=http%3A%2F%2Fwww.lavilotte-rolle.fr')




class FindPinTest(TestCase):
    """Find pin Test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # launch client
        self.client = Client()


    def test_urls(self):
        urls = [
            # user should be connected
            {
                'url': '/pin/find/?url=http%3A%2F%2Flavilotte-rolle.fr' +
                    '%2Fcontact%2F',
                'status': 302,
                'template': 'user/user_login.html',
            },
            {
                'url': '/pin/find/',
                'status': 302,
                'template': 'user/user_login.html',
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)

        urls = [
            {
                'url': '/pin/find/?url=http%3A%2F%2Flavilotte-rolle.fr' +
                    '%2Fcontact%2F',
                'status': 200,
                'template': 'pin/pin_find.html',
            },
            {
                'url': '/pin/find/',
                'status': 404,
                'template': '404.html',
            },
          
        ]
        test_urls(self, urls)


    def test_find_pin_context_with_html_resource(self):
        # login with user
        login(self, self.user)
        
        response = self.client.get(
                '/pin/find/?url=http%3A%2F%2Flavilotte-rolle.fr%2Ftmp%2Fpinpict_tests%2F')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_find.html')
        self.assertEqual(response.context['picts'], 
                [{'alt': '', 'href': 'http://lavilotte-rolle.fr/tmp/pinpict_tests/999.jpg'}])
        self.assertEqual(response.context['url'], 'http://lavilotte-rolle.fr/tmp/pinpict_tests/')


    def test_find_pin_context_with_image_resource(self):
        # login with user
        login(self, self.user)
        
        response = self.client.get(
                '/pin/find/?url=http%3A%2F%2Flavilotte-rolle.fr%2Ftmp%2Fpinpict_tests%2F999.jpg')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'pin/pin_find.html')
        self.assertEqual(response.context['picts'], 
                [{'alt': '', 'href': 'http://lavilotte-rolle.fr/tmp/pinpict_tests/999.jpg'}])
        self.assertEqual(response.context['url'], 'http://lavilotte-rolle.fr/tmp/pinpict_tests/999.jpg')


class PinPolicyTest(TestCase):
    """Test policy of pins."""
    def setUp(self):
        # create users
        create_test_users(self)
        # create resources
        create_test_resources(self)
        # create boards
        create_test_boards(self)
        # create pins
        create_test_pins(self)
        self.pin3 = Pin(
            resource = self.resource,
            board = self.board,
            description = 'test pin 3',
            pin_user = self.user,
        )
        self.pin3.save()
        self.pin4 = Pin(
            resource = self.resource,
            board = self.board,
            description = 'test pin 4',
            pin_user = self.user,
        )
        self.pin4.save()
        # launch client
        self.client = Client()

    def test_policy_create(self):
        # create a pin
        pin = Pin(
            resource = self.resource,
            board=self.board,
            description = 'test pin',
            pin_user = self.user,
        )
        pin.save()
        # assert it has same policy than it's board.
        self.assertEqual(pin.policy, self.board.policy)


    def test_policy_update(self):
        # login
        login(self, self.user)
        response = self.client.post('/flr/user-board/edit/', {
            'title': 'user board',
            'description': 'user board for tests',
            'policy': 0,
            }, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
            'board/board_list.html'
        )

        # assert board's pin policy have been updated
        pins = Pin.objects.filter(board=self.board)
        for pin in pins:
            self.assertEqual(pin.policy, 0)


        response = self.client.post('/flr/user-board/edit/', {
            'title': 'user board',
            'description': 'user board for tests',
            'policy': 1,
            }, follow=True
        )

        # assert board's pin policy have been updated
        pins = Pin.objects.filter(board=self.board)
        for pin in pins:
            self.assertEqual(pin.policy, 1)



