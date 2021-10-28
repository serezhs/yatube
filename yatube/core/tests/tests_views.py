from django.test.testcases import TestCase


from django.test import Client, TestCase


class CustomErrorsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_404error_template(self):
        response = self.guest_client.get('/unexiting_page/')
        self.assertTemplateUsed(response, 'core/404.html')
