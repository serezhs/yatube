from http import HTTPStatus

from django.contrib.auth import get_user_model
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
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage(self):
        """Страница / доступна любому пользователю"""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_page(self):
        """Страница /group/<slug>/ доступна люблму пользователю"""
        response = self.guest_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_page(self):
        """Страница /posts/post_id>/  доступна любому пользователю"""
        response = self.guest_client.get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_page(self):
        """Страница /profile/<username>/  доступна любому пользователю"""
        response = self.guest_client.get(f'/profile/{self.user.username}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexiting_page(self):
        """Страница /unexiting_page/ вернет ошибку 404"""
        response = self.guest_client.get('/unexiting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_page(self):
        """Страница /create/ доступна только авторизованному пользователю"""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_page(self):
        """Страница /posts/<post_id>/edit/ доступна только автору поста"""
        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_template(self):
        """Страница по адресу / использует шаблон posts/index.html."""
        response = self.authorized_client.get('/')
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_group_page_template(self):
        """
        Страница по адресу /group/<slug>/
        использует шаблон posts/group_list.html.
        """
        response = self.authorized_client.get(f'/group/{self.group.slug}/')
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_profile_page_template(self):
        """
        Страница по адресу /profile/<username>/
        использует шаблон posts/profile.html.
        """
        url = f'/profile/{self.user.username}/'
        response = self.authorized_client.get(url)
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_post_page_template(self):
        """
        Страница по адресу /posts/post_id>/
        использует шаблон posts/post_detail.html.
        """
        response = self.authorized_client.get(f'/posts/{self.post.id}/')
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_create_page_template(self):
        """
        Страница по адресу /create/
        использует шаблон posts/create_post.html.
        """
        response = self.authorized_client.get('/create/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_edit_page_template(self):
        """
        Страница по адресу /posts/<post_id>/edit/
        использует шаблон posts/create_post.html.
        """
        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
        self.assertTemplateUsed(response, 'posts/create_post.html')
