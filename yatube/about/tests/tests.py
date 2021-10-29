from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_techpage_and_authorpage(self):
        httpStatus_url = {
            HTTPStatus.OK: '/about/tech/',
            HTTPStatus.OK: '/about/author/',
        }
        for httpStatus, url in httpStatus_url.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, httpStatus)

    def test_authorpage_and_techpage_templates(self):
        templates_url_names = {
            'about/tech.html': '/about/tech/',
            'about/author.html': '/about/author/',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)
