from django.test import TestCase, Client

from user.models import User




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
        self.assertEqual(response.templates[0].name,
                'base.html')


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



