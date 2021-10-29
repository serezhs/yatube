from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_cache(self):
        """Тестирование кеша"""
        response = self.authorized_client.get(reverse('posts:index'))
        Post.objects.filter(text='Тестовый текст', author=self.user).delete()
        self.assertEqual(response.context.get('page_obj')[0], self.post)
        cache.clear()
        self.assertIsNot(response.context.get('page_obj')[0], self.post)
