from django.test import TestCase

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



