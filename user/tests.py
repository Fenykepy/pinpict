import os

from PIL import Image

from django.test import TestCase, Client
from django.core.files import File

from user.models import User
from pinpict.settings import RESERVED_WORDS, BASE_DIR, MEDIA_ROOT, AVATAR_MAX_SIZE




def test_urls(instance, urls):
    """Test urls."""
    for elem in urls:
        response = instance.client.get(elem['url'])
        instance.assertEqual(response.status_code, elem['status'])
        response = instance.client.get(elem['url'], follow=True)
        instance.assertEqual(response.templates[0].name, elem['template'])



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



def login(instance, user):
    """Login with given user, assert it's ok"""
    login = instance.client.login(username=user.username,
            password='top_secret')
    instance.assertEqual(login, True)



class UserLoginTest(TestCase):
    """User login test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # launch client
        self.client = Client()


    def test_urls(self):
        urls = [
            {
                'url': '/login/',
                'status': 200,
                'template': 'user/user_login.html',
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)
        urls = [
            {
                'url': '/login/',
                'status': 302,
                'template': 'board/board_list.html',
            },
        ]
        test_urls(self, urls)


    def test_login(self):
        """test user login."""
        response = self.client.post('/login/', {
            'username': 'flr',
            'password': 'top_secret',
        }, follow=True)
        
        # assert user is connected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, 'flr')
        self.assertEqual(response.templates[0].name,
                'board/board_list.html')


    def test_login_with_redirection(self):
        """test user login."""
        response = self.client.post('/login/?next=/', {
            'username': 'flr',
            'password': 'top_secret',
        }, follow=True)
        
        # assert user is connected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].username, 'flr')
        # user is redirected to his board page
        self.assertEqual(response.templates[0].name,
                'board/board_list.html')


    def test_login_with_wrong_password(self):
        """test user login."""
        response = self.client.post('/login/', {
            'username': 'flr',
            'password': 'error',
        })
        
        # assert user is connected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].is_authenticated(), False)
        self.assertEqual(response.templates[0].name,
                'user/user_login.html')


    def test_login_with_wrong_user(self):
        """test user login."""
        response = self.client.post('/login/', {
            'username': 'tom',
            'password': 'top_secret',
        })
        
        # assert user is connected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].is_authenticated(), False)
        self.assertEqual(response.templates[0].name,
                'user/user_login.html')


    def test_login_with_no_user(self):
        """test user login."""
        response = self.client.post('/login/', {
            'password': 'top_secret',
        })
        
        # assert user is connected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].is_authenticated(), False)
        self.assertEqual(response.templates[0].name,
                'user/user_login.html')


    def test_login_with_no_user(self):
        """test user login."""
        response = self.client.post('/login/', {
            'username': 'flr',
        })
        
        # assert user is connected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].is_authenticated(), False)
        self.assertEqual(response.templates[0].name,
                'user/user_login.html')





class UserLogoutTest(TestCase):
    """User logout test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # launch client
        self.client = Client()


    def test_urls(self):
        urls = [
            {
                'url': '/logout/',
                'status': 302,
                'template': 'user/user_login.html'
            },
        ]
        test_urls(self, urls)

    def test_logout(self):
        # login with user
        login(self, self.user)
        response = self.client.get('/logout/')
        # assert redirection is ok
        self.assertEqual(response.status_code, 302)
        # assert user isn't connected anymore
        self.assertEqual(hasattr(response.context, 'user'), False)

        response = self.client.get('/logout/', follow=True)
        # assert redirection is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name,
                'user/user_login.html')


class UserRegistrationTest(TestCase):
    """User registration test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # launch client
        self.client = Client()


    def test_urls(self):
        urls = [
            {
                'url': '/register/',
                'status': 200,
                'template': 'user/user_registration.html'
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)

        urls = [
            {
                'url': '/register/',
                'status': 302,
                'template': 'board/board_list.html',
            }
        ]
        test_urls(self, urls)


    def test_registration_normal(self):
        # try to register with normal data
        response = self.client.post('/register/', {
            'username': 'john',
            'password1': 'tom',
            'password2': 'tom',
            'email': 'john@john.com',
            }, follow=True
        )
        # assert redirection is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'board/board_list.html')
        self.assertEqual(response.context['user'].username, 'john')

        # assert user has been created
        user = User.objects.get(username='john')
        self.assertEqual(user.username, 'john')


    def test_registration_different_passwords(self):
        response = self.client.post('/register/', {
            'username': 'john',
            'password1': 'tom',
            'password2': 'toms',
            'email': 'john@john.com',
            }, follow=True
        )
        # assert form is served again
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'user/user_registration.html')

        # assert user hasn't been created
        user = User.objects.filter(username='john').count()
        self.assertEqual(user, 0)


    def test_registration_without_mail(self):
        response = self.client.post('/register/', {
            'username': 'john',
            'password1': 'tom',
            'password2': 'tom',
            }, follow=True
        )
        # assert form is served again
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'user/user_registration.html')

        # assert user hasn't been created
        user = User.objects.filter(username='john').count()
        self.assertEqual(user, 0)


    def test_registration_without_username(self):
        response = self.client.post('/register/', {
            'password1': 'tom',
            'password2': 'tom',
            'email': 'john@john.com',
            }, follow=True
        )
        # assert form is served again
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'user/user_registration.html')

        # assert user hasn't been created
        user = User.objects.filter(email='john@john.com').count()
        self.assertEqual(user, 0)


    def test_registration_without_password_confirmation(self):
        response = self.client.post('/register/', {
            'username': 'john',
            'password1': 'tom',
            #'password2': 'tom',
            'email': 'john@john.com',
            }, follow=True
        )
        # assert form is served again
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'user/user_registration.html')

        # assert user hasn't been created
        user = User.objects.filter(username='john').count()
        self.assertEqual(user, 0)


    def test_registration_with_existing_user_name(self):
        # try to register with existing user name
        response = self.client.post('/register/', {
            'username': 'flr',
            'password1': 'tom',
            'password2': 'tom',
            'email': 'john@john.com',
            }, follow=True
        )
        # assert form is served again
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'user/user_registration.html')

        # assert user hasn't been created
        user = User.objects.filter(username='flr').count()
        self.assertEqual(user, 1)


    def test_registration_with_reserved_words(self):
        for word in RESERVED_WORDS:
            response = self.client.post('/register/', {
                'username': word,
                'password1': 'tom',
                'password2': 'tom',
                'email': 'john@john.com',
                }, follow=True
            )
            # assert form is served again
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.templates[0].name, 'user/user_registration.html')

            # assert user hasn't been created
            user = User.objects.filter(username=word).count()
            self.assertEqual(user, 0)
            user = User.objects.filter(email='john@john.com').count()
            self.assertEqual(user, 0)



class UserProfilTest(TestCase):
    """User profil test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # launch client
        self.client = Client()


    def test_urls(self):
        urls = [
            # if user is not logged in, redirect to login page
            {
                'url': '/profil/',
                'status': 302,
                'template': 'user/user_login.html'
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)

        urls = [
            {
                'url': '/profil/',
                'status': 200,
                #'template': 'user/user_profil.html',
                'template': 'user/user_profil.html',
            },
        ]
        test_urls(self, urls)

    
    def test_update_user_profil(self):
        # login with user
        login(self, self.user)

        response = self.client.post('/profil/', {
            'email': 'new_mail@domain.com',
            'first_name': 'Fred',
            'last_name': 'Lavilotte-Rolle',
            'website': 'http://lavilotte-rolle.fr',
            'facebook_link': 'http://facebook.com',
            'flickr_link': 'https://www.flickr.com/photos/lavilotte-rolle/',
            'twitter_link': 'https://twitter.com/',
            'gplus_link': 'https://plus.google.com/',
            'pinterest_link': 'http://www.pinterest.com/fredericlavilot/',
            'vk_link': 'https://vk.com/',
            }, follow=True
        )
        # assert everything is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'board/board_list.html')

        user = User.objects.get(username=self.user.username)
        self.assertEqual(user.email, 'new_mail@domain.com')
        self.assertEqual(user.first_name, 'Fred')
        self.assertEqual(user.last_name, 'Lavilotte-Rolle')
        self.assertEqual(user.website, 'http://lavilotte-rolle.fr/')
        self.assertEqual(user.facebook_link, 'http://facebook.com/')
        self.assertEqual(user.flickr_link, 'https://www.flickr.com/photos/lavilotte-rolle/')
        self.assertEqual(user.twitter_link, 'https://twitter.com/')
        self.assertEqual(user.gplus_link, 'https://plus.google.com/')
        self.assertEqual(user.pinterest_link, 'http://www.pinterest.com/fredericlavilot/')
        self.assertEqual(user.vk_link, 'https://vk.com/')


    def test_update_user_profil_without_email(self):
        # login with user
        login(self, self.user)

        response = self.client.post('/profil/', {
            #'email': 'new_mail@domain.com',
            'first_name': 'Fred',
            'last_name': 'Lavilotte-Rolle',
            'website': 'http://lavilotte-rolle.fr',
            'facebook_link': 'http://facebook.com',
            'flickr_link': 'https://www.flickr.com/photos/lavilotte-rolle/',
            'twitter_link': 'https://twitter.com/',
            'gplus_link': 'https://plus.google.com/',
            'pinterest_link': 'http://www.pinterest.com/fredericlavilot/',
            'vk_link': 'https://vk.com/',
            }, follow=True
        )
        # assert form is served again
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'user/user_profil.html')

        # assert user still has mail
        user = User.objects.get(username=self.user.username)
        self.assertEqual(user.email, 'pro@lavilotte-rolle.fr')
    


    def test_upload_user_avatar(self):
        # login with user
        login(self, self.user)
        
        def post_avatar(follow):
            # post avatar file
            with open(os.path.join(BASE_DIR, 'user',
                'test_files', 'test_avatar.png'), 'rb') as avatar:
                return self.client.post('/profil/', {
                    'email': 'pro@lavilotte-rolle.fr',
                    'avatar': avatar, 
                    }, follow=follow
                )

        response = post_avatar(True)
        # assert everything is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'board/board_list.html')

        # assert user avatar has been store in db
        user = User.objects.get(username=self.user.username)
        avatar = False
        if user.avatar:
            avatar = True
        self.assertEqual(avatar, True)
        # assert file has been created
        file = os.path.join(MEDIA_ROOT, user.avatar.name)
        basename, ext = os.path.splitext(user.avatar.name)
        self.assertTrue(os.path.isfile(file))
        
        # assert avatar has been resized
        img = Image.open(file)
        self.assertTrue(img.size[0] > 1)
        self.assertTrue(img.size[0] <= AVATAR_MAX_SIZE)
        self.assertTrue(img.size[1] > 1)
        self.assertTrue(img.size[1] <= AVATAR_MAX_SIZE)

        # assert file equal to <user.id>.<file_format>
        #self.assertEqual(file, os.path.join(
        #    MEDIA_ROOT,
        #    "images/avatars",
        #    "{}{}".format(user.id, ext.lower()
        #)))
        

        # remove file
        os.remove(file)



class UserChangePasswordTest(TestCase):
    """User password changement test class."""

    def setUp(self):
        # create users
        create_test_users(self)
        # launch client
        self.client = Client()


    def test_urls(self):
        urls = [
            # if user is not logged in, redirect to login page
            {
                'url': '/profil/password/',
                'status': 302,
                'template': 'user/user_login.html'
            },
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)
        urls = [
            {
                'url': '/profil/password/',
                'status': 200,
                'template': 'board/board_forms.html'
            },
        ]
        test_urls(self, urls)


    def test_change_user_password(self):
        # login with user
        login(self, self.user)
        response = self.client.post('/profil/password/', {
            'password1': 'tata',
            'password2': 'tata',
            }, follow=True
        )

        # assert everything is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'board/board_list.html')

        # logout
        response = self.client.get('/logout/')

        # try to login with new password
        result = self.client.login(username=self.user.username,
            password='tata')
        self.assertTrue(result)

        # logout
        response = self.client.get('/logout/')

        # try to login with old password
        result = self.client.login(username=self.user.username,
                password='top_secret')
        self.assertEqual(result, False)



    def test_change_user_password_with_bad_confirmation_password(self):
        # login with user
        login(self, self.user)
        response = self.client.post('/profil/password/', {
            'password1': 'tata',
            'password2': 'tati',
            }, follow=True
        )

        # assert everything is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'board/board_forms.html')

        # logout
        response = self.client.get('/logout/')

        # try to login with new password
        result = self.client.login(username=self.user.username,
            password='tata')
        self.assertEqual(result, False)

        # logout
        response = self.client.get('/logout/')

        # try to login with new password
        result = self.client.login(username=self.user.username,
            password='tati')
        self.assertEqual(result, False)


        # logout
        response = self.client.get('/logout/')

        # try to login with old password
        result = self.client.login(username=self.user.username,
                password='top_secret')
        self.assertTrue(result)



    def test_change_user_password_without_confirmation_password(self):
        # login with user
        login(self, self.user)
        response = self.client.post('/profil/password/', {
            'password2': 'tati',
            }, follow=True
        )

        # assert everything is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'board/board_forms.html')

        # logout
        response = self.client.get('/logout/')

        # try to login with new password
        result = self.client.login(username=self.user.username,
            password='tata')
        self.assertEqual(result, False)

        # logout
        response = self.client.get('/logout/')

        # try to login with old password
        result = self.client.login(username=self.user.username,
                password='top_secret')
        self.assertTrue(result)



    def test_change_user_password_without_password(self):
        # login with user
        login(self, self.user)
        response = self.client.post('/profil/password/', {
            'password1': 'tati',
            }, follow=True
        )

        # assert everything is ok
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'board/board_forms.html')

        # logout
        response = self.client.get('/logout/')

        # try to login with new password
        result = self.client.login(username=self.user.username,
            password='tati')
        self.assertEqual(result, False)

        # logout
        response = self.client.get('/logout/')

        # try to login with old password
        result = self.client.login(username=self.user.username,
                password='top_secret')
        self.assertTrue(result)



class UserPasswordRecoveryTest(TestCase):
    """User password recovery test class."""
    pass

    def setUp(self):
        # create users
        create_test_users(self)
        # launch client
        self.client = Client()


    def test_urls(self):
        urls = [
            # if user is not logged in, serve form
            {
                'url': '/recovery/',
                'status': 200,
                'template': 'board/board_forms.html'
            },
            # if user bad uuid is requested, return 404
            {
                'url': '/recovery/f47ac10b-58cc-4372-a567-0e02b2c3d479/',
                'status': 404,
                'template': '404.html'
            }
        ]
        test_urls(self, urls)


    def test_logged_in_urls(self):
        # login with user
        login(self, self.user)
        urls = [
            # if user is logged in, redirect to password changement form
            {
                'url': '/recovery/',
                'status': 302,
                'template': 'board/board_forms.html'
            },
            # if user bad uuid is requested, return 404
            {
                'url': '/recovery/f47ac10b-58cc-4372-a567-0e02b2c3d479/',
                'status': 404,
                'template': '404.html'
            }
        ]
        test_urls(self, urls)












