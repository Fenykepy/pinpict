from django.test import TestCase, Client

from user.models import User
from pinpict.settings import RESERVED_WORDS




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




