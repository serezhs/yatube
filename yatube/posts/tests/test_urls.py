from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )
        cls.group = Group.objects.create(
            title='test',
            slug='test',
        )

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_url_available_for_all_users(self):
        httpStatus_url = {
            HTTPStatus.OK: '/',
            HTTPStatus.OK: f'/group/{self.group.slug}/',
            HTTPStatus.OK: f'/posts/{self.post.id}/',
            HTTPStatus.OK: f'/profile/{self.user.username}/',
            HTTPStatus.NOT_FOUND: '/unexiting_page/',
        }
        for httpStatus, url in httpStatus_url.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, httpStatus)


    def test_url_available_for_authorized_users(self):
        httpStatus_url = {
            HTTPStatus.OK: '/create/',
            HTTPStatus.OK: f'/posts/{self.post.id}/edit/',
        }
        for httpStatus, url in httpStatus_url.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, httpStatus)


    def test_posts_templates(self):
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{self.group.slug}/',
            'posts/profile.html': f'/profile/{self.user.username}/',
            'posts/post_detail.html': f'/posts/{self.post.id}/',
            'posts/create_post.html': '/create/',
            'posts/create_post.html': f'/posts/{self.post.id}/edit/',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template) 
