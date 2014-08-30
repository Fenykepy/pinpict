import os

from django.test import TestCase, Client
from django.core.files import File

from pinpict.settings import BASE_DIR
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





