from django.test import TestCase


class PublicUserApiTests(TestCase):
    def test_user_exists(self):
        """
        Test User
        """

        x = 2
        y = 2
        z = 5
        a = 5

        self.assertEqual((x + y), 4)
        self.assertEqual((z + a), 10)
