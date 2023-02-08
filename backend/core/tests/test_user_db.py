from django.test import TestCase


class PublicUserApiTests(TestCase):
    def test_user_exists(self):
        """
        Test User
        """

        x = 2
        y = 2

        self.assertEqual((x + y), 2)
